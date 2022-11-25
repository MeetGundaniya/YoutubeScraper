"""
Models for Storing data on sql and mongodb
"""

# LOCALFOLDER LIBRARY
from ._mongo import ChannelMongo, VideoMongo
from ._sql import Channel, Video



__all__ = [
  'Channel',
  'Video',
  'ChannelMongo',
  'VideoMongo',
]
