"""
Template filters to convert thing into human readable format
"""

# STDLIB LIBRARY
import logging
from datetime import datetime
from math import floor

# THIRDPARTY LIBRARY
import timeago

# DJANGO LIBRARY
from django import template
from django.utils.timezone import make_aware



logger = logging.getLogger(__name__)
register = template.Library()


@register.filter(is_safe=False)
def intword(value):
  """
  Convert number into human readable string
  """

  # if isinstance(value, str):
  #   nums = value.split(',')

  #   if len(nums[0]) <= 3:
  #     new_num = nums[0] + magnitudeDict[len(nums)-1]

  magnitudeDict = {0: '', 1: 'K', 2: 'M', 3: 'B', 4: 'T', 5: 'Q'}
  num = value if isinstance(value, int) else int(value)
  magnitude = 0

  while num >= 1000.0:
    num = num / 1000.0
    magnitude += 1

  new_num = f'{floor(num*100.0)/100.0}{magnitudeDict[magnitude]}'

  logger.debug(f'convert {num} into {new_num}')
  return new_num


@register.filter(is_safe=False)
def relative_date(value):
  """
  Calculate time duration between given datetime and current datetime to human readable format
  """
  try:
    return timeago.format(
      # value if value.tzinfo else value.replace(tzinfo=timezone.utc),
      # datetime.now(tz=timezone.utc),
      value if value.tzinfo else make_aware(value),
      make_aware(datetime.now()),
    )
  except:
    return value



@register.filter(is_safe=False)
def datestr(value):
  return datetime.strftime(value, '%b %d, %Y')
