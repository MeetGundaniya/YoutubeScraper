"""
This module handle request within ScraperApp
"""

# STDLIB LIBRARY
import logging

# DJANGO LIBRARY
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

# FIRSTPARTY LIBRARY
from backend.settings import env
from scraper.contrib import youtube
from scraper.helpers import ChannelDispenser, VideoDispenser



logger = logging.getLogger(__name__)


class HomeTemplateView(TemplateView):
  """
  Handle request for index page and it's contents
  """

  template_name = "scraper/index.html"

  def get(self, request, *args, **kwargs):
    self.extra_context = {'github_link': env.str('GITHUB_LINK', '#')}
    with ChannelDispenser() as cd:
      self.extra_context.update({'channels': cd.channel_list})
    response = super().get(request, *args, **kwargs)
    return response


class VideoTemplateView(TemplateView):
  """
  Handle request for videos page and it's contents
  """

  template_name = "scraper/video_list.html"

  def get(self, request, *args, **kwargs):
    self.extra_context = {'github_link': env.str('GITHUB_LINK', '#')}
    c_id = kwargs.get("c_id", None)
    if not c_id:
      return redirect(reverse('home'))

    with ChannelDispenser(url={"channel_id": c_id}) as cd:
      if cd.created:      
        messages.add_message(request, messages.WARNING, "Videos for this channel are not available")
        messages.add_message(request, messages.SUCCESS, "Request has been sent successfully")
        messages.add_message(request, messages.INFO, "Please, Try again in a few minutes")
        logger.info('new request sent to add videos for {}', f'channel_id={c_id}')
        return redirect(reverse('home'))
      
      else:
        self.extra_context.update({
          'channels': cd.channel_list,
          'channel': cd.channel_details,
          'videos': cd.videos_detail,
        })

        if not self.extra_context['videos']:
          messages.add_message(request, messages.WARNING, "A request for this channel's video has already been sent")
          messages.add_message(request, messages.INFO, "Please, wait for admin approval")

    response = super().get(request, *args, **kwargs)
    return response


class WatchTemplateView(TemplateView):
  """
  Handle request for player page and it's contents
  """

  template_name = "scraper/watch_video.html"

  def get(self, request, *args, **kwargs):
    v_id = request.GET.get("v", None)
    self.extra_context = {}

    with VideoDispenser(id=v_id) as vd:
      if vd.created:
        messages.add_message(request, messages.WARNING, "Video is not available")
        messages.add_message(request, messages.SUCCESS, "Request has been sent successfully")
        return redirect(reverse('home'))

      else:
        yv = youtube.Video(f'https://www.youtube.com/watch?v={v_id}')
        yv_parser = yv.video_info()
        self.extra_context['video_metadata'] = {
          **vd.video_details,
          'like_count': vd.video_like_count,
          'comment_count': vd.video_comment_count,
          'description': vd.video_description,
          'comments': yv_parser['comments'],
        }

        with ChannelDispenser(obj=vd.channel) as cd:
          self.extra_context.update({
            'channel': cd.channel_details,
            'videos': cd.videos_detail,
          })

        self.extra_context["video_streams"] = yv.video_streams()

    self.extra_context["css_class"] = {"main": "watch"}

    response = super().get(request, *args, **kwargs)
    return response



class SearchTemplateView(TemplateView):
  """
  Handle request for search query
  """
  
  logger = logging.LoggerAdapter(logger)
  template_name = "scraper/video_list.html"

  def get(self, request, *args, **kwargs):
    self.extra_context = {'github_link': env.str('GITHUB_LINK', '#')}
    search_query = request.GET.get("search_query", None)

    if not search_query:
      messages.add_message(request, messages.ERROR, f'search box can\'t be empty')
      return redirect(reverse('home'))

    ys = youtube.Search(search_query, recommended=True)

    self.extra_context = {
      'videos': ys.video_generator(),
      'search_query': search_query,
      'token_name': 'search_token',
    }

    response = super().get(request, *args, **kwargs)
    # response.delete_cookie(self.extra_context['token_name'])
    response.set_cookie(self.extra_context['token_name'], ys.parser['continuation']['token'])
    return response

  def post(self, request, *args, **kwargs):
    search_query = request.GET.get("search_query", None)
    continuation_token = request.POST.get("continuation_token", None)

    ys = youtube.Search(search_query, token=continuation_token, recommended=True)
    self.extra_context = {
      'videos': ys.video_generator(),
      'token_name': 'search_token',
    }

    context = self.get_context_data(**kwargs)
    response = self.render_to_response(context)

    response.set_cookie(self.extra_context['token_name'], ys.parser['continuation']['token'])
    return response

  def get_template_names(self):
    if self.request.method == 'POST':
      return ['scraper/includes/video_grid.html']
    return super().get_template_names()

  @method_decorator(csrf_exempt)
  def dispatch(self, *args, **kwargs):
    return super().dispatch(*args, **kwargs)

