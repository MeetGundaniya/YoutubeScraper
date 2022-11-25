"""
Models for Storing data on sql
"""

# THIRDPARTY LIBRARY
from djongo import models

# DJANGO LIBRARY
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _



def validate_human_readable_number(num):
  message = f'{num} is not valid value'
  return RegexValidator('\d{0,3}\.\d{0,2}(K|M|B|T|Q){1}', message)


class Video(models.Model):
  """
  Store video data on sql
  """

  video_id = models.CharField(unique=True, max_length=32)
  title = models.CharField(unique=True, blank=True, max_length=128)
  length = models.DurationField(null=True)
  published_at = models.DateTimeField(null=True)
  view_count = models.CharField(null=True, max_length=8, validators=[validate_human_readable_number])
  like_count = models.CharField(null=True, max_length=8, validators=[validate_human_readable_number])
  comment_count = models.CharField(null=True, max_length=8)
  last_updated = models.DateTimeField(auto_now=True)
  channel = models.ForeignKey(to='scraper.Channel', related_name='videos', on_delete=models.CASCADE, null=True)

  class Meta:
    verbose_name = 'Video'
    ordering = ('channel', '-published_at', '-view_count', '-like_count', '-comment_count')

  def __repr__(self):
    return f'<VideoModel: video_id={self.video_id}, title={self.title}, channel={self.channel}>'

  def __str__(self):
    return f'Video(id={self.video_id})'


class Channel(models.Model):
  """
  Store Channel data on sql
  """

  channel_id = models.CharField(unique=True, blank=True, max_length=32)
  custom_url = models.CharField(unique=True, blank=True, max_length=32)
  title = models.CharField(blank=True, max_length=128)
  subscriber = models.CharField(null=True, max_length=8, validators=[validate_human_readable_number])
  last_updated = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = 'Channel'
    unique_together = ('channel_id', 'custom_url')

  def __repr__(self):
    return f'<ChannelModel: channel_id={self.channel_id}, title={self.title}>'

  def __str__(self):
    return f'Channel(id={self.channel_id})'

  def clean(self):
    if not self.channel_id and not self.custom_url:
      raise ValidationError(
        {
          'channel_id': 'channel_id and custom_url not allow blank togather',
          'custom_url': 'Even one of channel_id or custom_url should have a value',
        }
      )

