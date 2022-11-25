"""
Endpoint for accessing Youtube API
"""

# STDLIB LIBRARY
import logging

# THIRDPARTY LIBRARY
from googleapiclient.discovery import build

# FIRSTPARTY LIBRARY
from backend.settings import env



logger = logging.getLogger(__name__)


class Youtube:
  __youtube = build('youtube', 'v3', developerKey=env.str("YT_API_KEY"))

  @property
  def youtube(self):
    """
    Youtube singleton object
    """
    return self.__youtube


  def __call_api(self, request_for=None, **kwargs):
    """
    Hit YoutubeAPI for <request_for>
    """

    if not request_for:
      raise Exception('parameter \'request_for\' must not be None')
    
    try:
      logger.debug(f'getting Youtube singleton object', extra={'param': f'{request_for=}'})
      youtube = getattr(self.youtube, request_for)

      logger.debug(f'fetching data from Youtube API', extra={'param': f'{kwargs=}'})
      request = youtube().list(**kwargs)
      
      logger.debug(f'executing Youtube API', extra={'param': f'{request=}'})
      response = request.execute()

      logger.info('fetched youtube API successfully')
    
    except:
      logger.exception('failed to fetch data from Youtube API')
      return {}

    else:
      return response['items']


  def get_channel_detail(self, channels_ids=None, custom_url=None):
    """ Quota Cost: 1
    Fetch channel details for given channel id
    """
    return self.__call_api('channels', 
      part='id,snippet,statistics', 
      id=','.join(channels_ids)
    )


  def get_videos_id_from_channel(self, c_id):
    """ Quota Cost: 100
    Fetch videos id from given channel
    """
    return self.__call_api('search', 
      part='id', 
      channelId=c_id, 
      order='date', 
      type='video'
    )


  def get_videos_details_from_videos_id(self, v_ids):
    """ Quota Cost: 1
    Fetch videos details for given videos_id
    """
    return self.__call_api('channels', 
      part='snippet,contentDetails,statistics', 
      id=','.join(v_ids)
    )


  def get_video_comments_from_video_id(self, v_id):
    """ Quota Cost: 1
    Fetch video comments for given video_id
    """
    return self.__call_api('commentThreads', 
      part='snippet,id', 
      order='time', 
      videoId=v_id
    )
