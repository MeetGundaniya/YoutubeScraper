"""
Implements a simple wrapper around httpx
"""

# STDLIB LIBRARY
import asyncio
import logging

# THIRDPARTY LIBRARY
import httpx

# FIRSTPARTY LIBRARY
from core.helpers.exception import NotSupported



logger = logging.getLogger(__name__)

class Request:
  """
  Perform multiple requests concurrently
  """
  
  logger = logging.LoggerAdapter(logger)

  def __init__(self, url, method='GET', headers=None, params=None, postdata=None) -> None:
    self.url = url
    self.headers = headers
    self.params = params
    self.postdata = postdata or {}
    self.method = method

  def __call__(self, params=None, postdata=None):
    initial = {
      'url': self.url,
      'method': self.method,
      'headers': self.headers,
    }
    if not (params or postdata):
      raise TypeError('either params or postdata require')
    if params:
      initial['params'] = params
    if postdata:
      initial['postdata'] = postdata
    return self.__class__(**initial)

  def __setattr__(self, name, value):

    match name:
      case 'url' if not value.lower().startswith("http"):
        raise NotSupported(f'{value.split("://")[0]} not supported, possible value is "http"')
      case 'method' if self.postdata and value not in ['POST']:
        raise NotSupported(f'{value} request not supported to POST data')
      case 'headers':
        pass
      case 'params':
        pass
      case 'postdata' if not (isinstance(value, (bytes, str, dict)) or value is None):
        raise TypeError(f'"postdata" must be bytes, str, dict or None typed object, not {type(value)}')
 
    super().__setattr__(name, value)

  @property
  def _request_param(self):
    param = {
      'method': self.method, 
      'url': self.url, 
      'params': self.params,
      'content': bytes(str(self.postdata or ''), encoding="utf-8"),
      'follow_redirects': True,
    }
    self.logger.debug('{}', f'{param}')
    return param

  async def _execute_request(self):
    async with httpx.AsyncClient(headers=self.headers) as client:
      return await client.request(**self._request_param)
    
  def result(self):
    response = asyncio.run(self._execute_request())
    return self.validate_response(response)

  @classmethod
  async def _execute_all_request(cls, collection):
    async with httpx.AsyncClient() as client:
      tasks = []
      for req in collection:
        if isinstance(req, cls):
          tasks.append(client.request(**req._request_param, headers=req.headers))
        else:
          cls.logger.error(f'{req} must be {cls} instance, not {type(req)}')

      return await asyncio.gather(*tasks)

  @classmethod
  def results(cls, collection):
    responses = asyncio.run(cls._execute_all_request(collection))
    for response in responses:
      yield cls.validate_response(response)

  @staticmethod
  def validate_response(response):
    if response.status_code!=200:
      print(f'{response.text=}\n')
      response.raise_for_status()
    return response.text
