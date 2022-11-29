"""
Utility functions
"""

# STDLIB LIBRARY
import contextlib
import cProfile
import functools
import inspect
import logging
import pstats
from datetime import datetime, timedelta



logger = logging.getLogger(__name__)


def lrc_cache(maxsize=None, maxtime=86400, typed=False):
  """
  Least-recently-call cache decorator.
  """

  def wrapper_cache(func):
    cached_func = functools.lru_cache(maxsize=maxsize, typed=typed)(func)
    cached_func.lifetime = timedelta(seconds=maxtime)
    cached_func.expiration = datetime.utcnow() + cached_func.lifetime

    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
      if kwargs.get('cache', True):
        func_call_args = dict(sorted(inspect.getcallargs(func, *args, **kwargs).items(), key=lambda item: item[0]))

        if datetime.utcnow() >= cached_func.expiration:
          cached_func.cache_clear()
          cached_func.expiration = datetime.utcnow() + cached_func.lifetime

        result = cached_func(**func_call_args)
        logger.debug('', extra={'param': f'cache_info={cached_func.cache_info()}'})
        return result

      else:
        return func(*args, **kwargs)

    for attr in ('cache_clear', 'cache_info', 'cache_parameters', 'lifetime', 'expiration'):
      setattr(wrapped_func, attr, getattr(cached_func, attr))

    return wrapped_func

  if callable(maxsize):
    func, maxsize = maxsize, None
    wrapper = wrapper_cache(func)
  else:
    wrapper = wrapper_cache

  logger.debug('Enable caching {}', f'lrc_cache({maxsize=}, {maxtime=}, {typed=})')
  return wrapper


def format_duration(length):
  """
  Convert timedelta object to human readable format (HH:MM:SS)
  """

  length = length if isinstance(length, int) else length.total_seconds()

  minutes, seconds = map(int, divmod(length, 60))
  hours, minutes = map(int, divmod(minutes, 60))

  total_time = ''
  if hours:
    total_time += f'{hours:02}:'
  if hours or minutes:
    total_time += f'{minutes:02}:'
  total_time += f'{seconds:02}'

  logger.debug(f'convert {length} to {total_time}')
  return total_time


@contextlib.contextmanager
def cprofiling(n_fun=20):
  print('\n\n')
  with cProfile.Profile() as pr:
    yield pr
  stats = pstats.Stats(pr)
  stats.sort_stats(pstats.SortKey.TIME)
  stats.print_stats(n_fun)
  print('\n')


__all__ = [
  'lrc_cache',
  'format_duration',
  'cprofiling',
]
