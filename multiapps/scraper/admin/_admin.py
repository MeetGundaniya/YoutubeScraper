"""
ModelAdmin for Admin interface
"""

# STDLIB LIBRARY
import logging

# DJANGO LIBRARY
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

# FIRSTPARTY LIBRARY
from scraper.models import Channel, Video

# LOCALFOLDER LIBRARY
from ._actions import (
    get_channels_videos,
)
from ._inlines import (
    ChanneMongolInlineAdmin,
    VideoInlineAdmin,
    VideoMongoInlineAdmin,
)



logger = logging.getLogger(__name__)


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
  """
  Admin interface for Channel model of sql
  """

  list_display = ('title', 'channel_id', 'custom_url', 'subscriber', 'last_updated')
  list_display_links = ('channel_id', 'custom_url', 'title')
  search_fields = ('title', 'channel_id')
  readonly_fields = ('last_updated',)

  inlines = [ChanneMongolInlineAdmin, VideoInlineAdmin]
  actions = [get_channels_videos]

  fieldsets = (
    (None, {'fields': (('channel_id', 'custom_url'), 'title')}),
    (
      'Statistics',
      {
        # 'classes': ('collapse',),
        'fields': ('subscriber', 'last_updated'),
      },
    ),
  )


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
  """
  Admin interface for Video model of sql
  """

  __logger = logging.LoggerAdapter(logger)
  
  @property
  def logger(self):
    if not (self.__logger.extra and self.__logger.extra.get('classname', None)):
      self.__logger.extra = {'classname': self.__class__.__name__}
    return self.__logger

  list_display = (
    'title',
    'video_id',
    'length',
    'published_at',
    'view_count',
    'like_count',
    'comment_count',
    'last_updated',
    'get_channel_name_from_video',
  )
  readonly_fields = ('video_id', 'length', 'published_at', 'view_count', 'like_count', 'comment_count', 'last_updated')
  search_fields = ('title', 'video_id')
  list_filter = ('channel__title', )

  inlines = [VideoMongoInlineAdmin]

  fieldsets = (
    (None, {'fields': ('video_id', 'title')}),
    (
      'Statistics',
      {
        # 'classes': ('collapse',),
        'fields': (('length', 'published_at'), ('view_count', 'like_count', 'comment_count'), 'last_updated'),
      },
    ),
  )

  @admin.display(description='Channel title')
  def get_channel_name_from_video(self, obj):

    try:
      related_link = mark_safe(f'<a href="{reverse("admin:scraper_channel_change", args=(obj.channel.id,))}">{obj.channel.title}</a>')
    except AttributeError as e:
      self.logger.warning('can not create hyperlink for channel due to {}', e.args)
      related_link = mark_safe(f'<a href="{reverse("admin:scraper_channel_changelist")}">Unknown</a>')

    return format_html("{}", related_link)
