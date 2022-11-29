"""
Supporting classes of different requests
"""

# STDLIB LIBRARY
import logging

# THIRDPARTY LIBRARY
import pytube

# FIRSTPARTY LIBRARY
from core.helpers.async_http import Request

# LOCALFOLDER LIBRARY
from ._parser import DataParser



__all__ = [
  'Video',
  'Channel',
  'Search'
]

class Youtube:
  """
  Base class for configure endpoints
  """
  __default_clients = {
    'WEB': {
      'context': {
        'client': {
          'clientName': 'WEB',
          'clientVersion': '2.20221110.08.00'
        }
      },
      'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'
    },
    'ANDROID': {
      'context': {
        'client': {
          'clientName': 'ANDROID',
          'clientVersion': '16.20'
        }
      },
      'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'
    }
  }

  base_api = 'https://www.youtube.com/youtubei/v1'
  base_headers = {
    'User-Agent': 'Mozilla/5.0', 
    'accept-language': 'en-US,en'
  }

  def __init__(self, client='WEB', **kwargs):
    self.api_key = self.__default_clients[client]['api_key']
    self.context = self.__default_clients[client]['context']
    self._request = {}
    self.base_params = {
      'key': self.api_key,
      'contentCheckOk': True,
      'racyCheckOk': True
    }
    self._html = ''
    self.parsed_data = {}

  def _payload_request(self, endpoint, method='GET', headers=None, params=None, postdata=None):
    params = params or {}
    params.update(self.base_params)

    headers = headers or {}
    headers.update({**self.base_headers})

    if method=='POST':
      endpoint_url = f'{self.base_api}{endpoint}'
      postdata = postdata or {}
      postdata.update({'context': self.context})
      headers.update({'content-type': 'application/json'})

    else:
      endpoint_url = endpoint

    return Request(endpoint_url, method, headers, params, postdata)


class Video(Youtube):
  """
  Endpoint for watch video
  """
  def __init__(self, url, token=None, **kwargs):
    self.url = url
    self.continuation = token or None
    super().__init__(**kwargs)

  def _watch_payload(self):
    req = self._request.get('watch', None)

    if req and self.continuation and req.method=='POST':
      req.postdata['continuation'] = self.continuation 

    elif req or self.continuation:
      req = self._request['watch'] = self._payload_request(
        endpoint= '/next',
        method= 'POST',
        postdata= {'continuation': self.continuation}
      )

    else:
      req = self._request['watch'] = self._payload_request(self.url)

    return req

  def video_info(self):
    """
    published_date,
    relative_published_date,
    title,
    short_view_count,
    view_count,
    like_count,
    comment_count,
    description,
    channel: [
      subscriber,
      thumbnail,
      title,
    ],
    comments: [
      id,
      text,
      relative_published_date,
      vote_count,
      author: [
        id,
        title,
        thumbnail_url,
      ],
    ]
    """
    parser = {}
    for _ in range(2):
      req = self._watch_payload()
      self.html = req.result()
      parser = DataParser(html=self.html, initial=parser)
      self.continuation = parser['continuation']['token']

    return parser['watch_result']

  def video_streams(self):
    """
    Get video streams to download video
    """

    pyt_obj = pytube.YouTube(url=self.url)

    video_streams = []
    for stream in pyt_obj.streams.filter(file_extension='mp4', type="video").order_by('resolution').desc():
      try:
        video_streams.append({
          'size': f'{stream.filesize/10**6:.2f}MB',
          'progressive': stream.is_progressive,
          'resolution': stream.resolution,
          'fps': f'{stream.fps}FPS',
          'url': stream.url,
        })
      except:
        continue

    return video_streams


class Channel(Youtube):
  """
  Endpoint for Channel
  """
  def __init__(self, url, max_reload=0, token=None, **kwargs):
    self.url = url
    self.max_reload = max_reload if max_reload > 0 else 1
    self.continuation = token or None
    self._html = None
    super().__init__(**kwargs)

  def _about_payload(self):
    req = self._request.get('about', None)
    if req is None:
      req = self._request['about'] = self._payload_request(f'{self.url}/about')
    return req

  def _videos_payload(self):
    req = self._request.get('video', None)

    if req and self.continuation and req.method=='POST':
      req.postdata['continuation'] = self.continuation 

    elif req or self.continuation:
      req = self._request['video'] = self._payload_request(
        endpoint= '/browse',
        method= 'POST',
        postdata= {'continuation': self.continuation}
      )

    else:
      req = self._request['video'] = self._payload_request(f'{self.url}/videos')

    return req

  def about(self):
    """ Fields: [
      id,
      canonical_url,
      title,
      view_count,
      subscribers ]
      avatar,
      description,
      country,
      joined,
    """
    req = self._about_payload()
    self.html = req.result()
    parser = DataParser(html=self.html)
    # return parser
    return parser['channelAboutRenderer']

  def video_generator(self):
    """ Fields: [
      id,
      title,
      view_count,
      length,
      thumbnail_url,
      published_at,
      moving_thumbnail_url,
      description,
      channel:[ id canonical_url title thumbnail_url ]]
    """

    for _ in range(self.max_reload):
      req = self._videos_payload()
      self.html = req.result()
      parser = DataParser(html=self.html)
      self.continuation = parser['continuation']['token']

      yield from parser['videoRenderer']


class Search(Youtube):
  """
  Endpoint for Search query
  """
  def __init__(self, search_query, recommended=False, max_reload=0, token=None, **kwargs):
    self.search_query = search_query
    self.recommended = recommended
    self.max_reload = max_reload if max_reload > 0 else 1
    self.continuation = token or None
    super().__init__(**kwargs)

  def search_payload(self):
    req = self._request.get('search', None)

    if req and self.continuation and req.method=='POST':
      req.postdata['continuation'] = self.continuation 

    elif req or self.continuation:
      req = self._request['search'] = self._payload_request(
        endpoint='/search',
        method='POST',
        params={'search_query': self.search_query},
        postdata={'continuation': self.continuation}
      )

    else:
      req = self._request['search'] = self._payload_request(
        'https://www.youtube.com/results',
        params={'search_query': self.search_query}
      )

    return req

  @property
  def parser(self):
    if not hasattr(self, '_parser'):
      self._parser = {}
      for _ in range(self.max_reload):
        req = self.search_payload()
        self.html = req.result()
        self._parser = DataParser(html=self.html, initial=self._parser)
        self.continuation = self._parser['continuation']['token']

    return self._parser


  def video_generator(self):
    """ Fields: [
      id,
      title,
      view_count,
      length,
      thumbnail_url,
      published_at,
      moving_thumbnail_url,
      description,
      published_at,
      channel:[ id canonical_url title thumbnail_url ]]
    """

    if self.recommended and 'shelfRenderer' in self.parser:
      for sr in self.parser['shelfRenderer']:
        yield from sr
    yield from self.parser['videoRenderer']
