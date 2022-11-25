"""
Extract channel and video details from databses
"""


# STDLIB LIBRARY
import logging
from contextlib import suppress

# FIRSTPARTY LIBRARY
from core.helpers.utils import format_duration
from scraper.models import Channel, Video



logger = logging.getLogger(__name__)


class VideoDispenser:
  """
  Extract video details from database
  """

  logger = logging.LoggerAdapter(logger)
  model = Video

  def __init__(self, id=None, obj=None, *args, **kwargs) -> None:
    if id:
      self.obj, self.created = self.model.objects.get_or_create(video_id=id, defaults={'video_id':id})
    elif isinstance(obj, self.model):
      self.obj = obj
    elif obj is not None:
      raise Exception(f'either video_id must be str or video_obj must be object of {self.model}')

  def __enter__(self):
    with suppress(AttributeError):
      self.logger.debug('extracting {}\'s details', f'video={self.obj}')
    return self

  def __exit__(self, *exc_args):
    if any(exc_args):
      self.logger.exception('failed to extract video details', exc_info=exc_args)
      return not getattr(self, 'propagate', True)
    else:
      self.logger.info('extracted videos details')

  @property
  def video_id(self):
    return self.obj.video_id

  @property
  def video_title(self):
    return self.obj.title

  @property
  def video_view_count(self):
    return self.obj.view_count

  @property
  def video_like_count(self):
    return self.obj.like_count

  @property
  def video_comment_count(self):
    return self.obj.comment_count

  @property
  def video_publish_at(self):
    return self.obj.published_at

  @property
  def video_length(self):
    return format_duration(self.obj.length)

  @property
  def video_thumbnail_url(self):
    return self.obj.from_mongo_video.thumbnail_url

  @property
  def video_description(self):
    return self.obj.from_mongo_video.mv_description

  @property
  def videos_groupby_channel(self):
    pass

  @property
  def video_details(self):
    try:
      self.logger.debug(f'extracting video details', extra={'param': f'{self.obj=}'})
      video = {
        'id': self.video_id,
        'title': self.video_title,
        'view_count': self.video_view_count,
        'published_at': self.video_publish_at,
        'length': self.video_length,
        'thumbnail_url': self.video_thumbnail_url,
      }

    except Exception as e:
      self.logger.exception('failed to extract video details', extra={'param': f'{self.obj=}'}, exc_info=e)
      video = {}

    else:
      self.logger.info(f'extracted video details')

    return video

  @property
  def channel(self):
    return self.obj.channel


class ChannelDispenser:
  """
  Extract channel details from database
  """
  
  logger = logging.LoggerAdapter(logger)
  model = Channel

  def __init__(self, url=None, obj=None, *args, **kwargs):
    if obj:
      self.obj, self.created = obj, False
    elif url:
      self.obj, self.created = self.model.objects.get_or_create(**url, defaults=url)

  def __enter__(self):
    with suppress(AttributeError):
      self.logger.debug('extracting {}\'s details', f'channel={self.obj}')
    return self

  def __exit__(self, *exc_args):
    if any(exc_args):
      self.logger.exception('failed to extract channel details', exc_info=exc_args)
      return not getattr(self, 'propagate', True)
    else:
      self.logger.info('extracted channel details')

  @property
  def get_queryset(self):
    return self.model.objects

  @property
  def channel_id(self):
    return self.obj.channel_id

  @property
  def channel_title(self):
    return self.obj.title

  @property
  def channel_thumbnail_url(self):
    return self.obj.from_mongo_channel.thumbnail_url

  @property
  def channel_subscriber(self):
    return self.obj.subscriber

  @property
  def channel_list(self):
    try:
      self.logger.debug(f'extracting channel_id and title')
      result = self.model.objects.values('channel_id', 'title')
    
    except Exception as e:
      self.logger.exception(f'failed to extract channel_id and title', exc_info=e)
      result = {}
    
    else:
      self.logger.info(f'extracted channel_id and title')

    return result

  @property
  def channel_details(self):
    try:
      self.logger.debug(f'extracting channel details', extra={'param': f'{self.obj=}'})
      channel = {
        'id': self.channel_id,
        'title': self.channel_title,
        'profile_url': self.channel_thumbnail_url,
        'subscriber': self.channel_subscriber,
      }

    except Exception as e:
      self.logger.exception('failed to extract channel details', extra={'param': f'{self.obj=}'}, exc_info=e)
      channel = {}

    else:
      self.logger.info(f'extracted channel details')

    return channel

  @property
  def videos_detail(self):
    videos = []

    for obj in self.obj.videos.iterator():
      with VideoDispenser(obj=obj) as vd:
        videos.append(vd.video_details)

    self.logger.info('extracted {} videos details', len(videos))

    return videos
