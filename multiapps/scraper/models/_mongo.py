"""
Models for Storing data on sql
"""

# THIRDPARTY LIBRARY
from djongo import models



class VideoMongo(models.Model):
  """
  Store Video data on mongodb
  """

  m_video = models.OneToOneField(to='scraper.Video', related_name='from_mongo_video', on_delete=models.PROTECT)
  mv_description = models.TextField()
  thumbnail_url = models.URLField()

  class Meta:
    verbose_name = 'Video OnMongoDB'

  _database = {
    'using': 'mongodb',
    'relation': ['scraper.Video']
  }

  def __repr__(self):
    return f'<VideoMongoModel: m_video={self.m_video}>'

  # def __str__(self):
  #   return f'VideoMongo(id={self.m_video})'


class ChannelMongo(models.Model):
  """
  Store Channel data on mongodb
  """

  # _id = models.ObjectIdField(primary_key=False, auto_created=False)
  m_channel = models.OneToOneField(to='scraper.Channel', related_name='from_mongo_channel', on_delete=models.PROTECT)
  description = models.TextField()
  thumbnail_url = models.URLField()
  # videos = models.EmbeddedField(
  #   model_container=VideoMongo
  # )

  class Meta:
    verbose_name = 'About Channel'

  _database = {
    'using': 'mongodb',
    'relation': ['scraper.Channel']
  }

  def __repr__(self):
    return f'<ChannelMongoModel: m_channel={self.m_channel}, thumbnail_url={self.thumbnail_url}>'

  # def __str__(self):
  #   return f'ChannelMongo(id={self.m_channel})'
