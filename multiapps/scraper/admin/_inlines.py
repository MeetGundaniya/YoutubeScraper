"""
Inline admin interface for respective models
"""

# DJANGO LIBRARY
from django.contrib import admin

# FIRSTPARTY LIBRARY
from scraper.models import ChannelMongo, Video, VideoMongo



class ChanneMongolInlineAdmin(admin.StackedInline):
  """
  Inline admin interface for Channel model from mongodb
  """

  model = ChannelMongo
  extra = 1
  can_delete = False
  show_change_link = True


class VideoMongoInlineAdmin(admin.StackedInline):
  """
  Inline admin interface for Video model from mongodb
  """

  model = VideoMongo
  extra = 1
  can_delete = False
  show_change_link = True


class VideoInlineAdmin(admin.TabularInline):
  """
  Inline admin interface for Video model from sql
  """

  model = Video
  extra = 1
  can_delete = False
  show_change_link = True
  readonly_fields = ('video_id', 'length', 'published_at', 'view_count', 'like_count', 'comment_count')

