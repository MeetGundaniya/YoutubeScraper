"""
Custom 'Formatter for logging module
"""

# STDLIB LIBRARY
import functools
import logging

# FIRSTPARTY LIBRARY
from multiapps.core.helpers.utils import lrc_cache



@functools.wraps(logging.LoggerAdapter, updated=())
class LoggerAdapter(logging.LoggerAdapter):
  def process(self, msg, kwargs):
    kwargs['extra'] = {**(self.extra or {}), **kwargs.get('extra', {})}
    return msg, kwargs

  def __set_name__(self, owner, name):
    self.extra = {'classname': owner.__name__}

  def __get__(self, obj, objtype=None):
    return self

  def __set__(self, obj, value):
    if isinstance(value, dict):
      self.extra.update(value)
    else:
      raise TypeError(f'value must be dict type, not {type(value)}')
      
setattr(logging, 'LoggerAdapter', LoggerAdapter)



class ColoredFormatter(logging.Formatter):
  """
  Responsible for colored log record
  """

  COLOR_CODE = {
    'level': {
      'CRITICAL': 196,
      'ERROR': 197,
      'WARNING': 208,
      'INFO': 27,
      'DEBUG': 51,
      'NOTSET': 15,
    },
    'exception': 124,
    'name': 221,
    'classname': 203,
    'funcName': 41,
    'lineno': 200,
    'message': 15,
    'param': 117,
    'stack_info': 229,
  }

  def __init__(self, fmt=None, datefmt=None, style='{', validate=True, *, defaults=None, colorize=None):
    self.fmt = fmt
    self.datefmt = datefmt
    self.validate = validate
    self.defaults = defaults
    self.colorize = colorize

  @lrc_cache(maxsize=64)
  def formatValidation(self, fmt, validate=True):
    self._style = logging.StrFormatStyle(fmt, defaults=self.defaults)
    if validate:
      self._style.validate()
    self._fmt = self._style._fmt

  # @lrc_cache(maxsize=20, maxtime=432000)
  @lrc_cache(maxtime=432000)
  def getColor(self, code=None, bg=False, bold=False, placeholder=True, clear=False):
    fmt = ''
    if isinstance(code, int):
      bg = '4' if bg else '3'
      fmt += f"\u001b[{bg}8;5;{code}m"
    if bold:
      fmt += '\u001b[1m'
    if placeholder:
      fmt += '{}'
    if clear:
      fmt += '\u001b[0m'
    return fmt

  def get_logs_fmt(self, levelname):
    return r''.join([
      self.getColor(code=self.COLOR_CODE['level'][levelname]).format('[{asctime} {levelname:^8}] ( '),
      self.getColor(code=self.COLOR_CODE['name'], clear=True).format('{name}'),
      self.getColor(bold=True).format(' : '),
      self.getColor(code=self.COLOR_CODE['classname'], clear=True).format('{classname}'),
      self.getColor(bold=True).format(' : '),
      self.getColor(code=self.COLOR_CODE['funcName'], clear=True).format('{funcName}'),
      self.getColor(bold=True).format(' : '),
      self.getColor(code=self.COLOR_CODE['lineno'], clear=True).format('{lineno}'),
      self.getColor(code=self.COLOR_CODE['level'][levelname]).format(' ) '),
      self.getColor(code=self.COLOR_CODE['message']).format('{message}'),
      self.getColor(code=self.COLOR_CODE['param']).format(' {param}'),
      self.getColor(placeholder=False, clear=True),
    ])

  def formatException(self, ei):
    dash_line = '-'*120
    exc_info = super().formatException(ei)
    return self.getColor(code=self.COLOR_CODE['exception'], clear=True).format(dash_line+'\n'+exc_info+'\n'+dash_line)

  def formatStack(self, si):
    stack_info = super().formatStack(si)
    return self.getColor(code=self.COLOR_CODE['stack_info'], clear=True).format(stack_info)

  def formatParam(self, record):
    param = getattr(record, 'param', '')
    if not isinstance(param, str):
      raise Exception(f"'param' must be str, not {type(param)}")
    return param

  def format(self, record):
    if record.args and record.name.split('.')[0] in ('scraper', 'core'):
      args = map(lambda arg: self.getColor(code=self.COLOR_CODE['param'], clear=True).format(arg), record.args)
      record.msg = record.msg.format(*args)
      record.args = None

    if getattr(record, 'classname', None) is None:
      record.classname = '---' or 'classname'

    record.param = self.formatParam(record)

    if self.colorize:
      fmt = self.get_logs_fmt(record.levelname)
    else:      
      fmt = self.fmt or r'[{asctime} {levelname:^8}] ( {name}:{classname}:{funcName}:{lineno} ) {message} {param}'
      
    self.formatValidation(fmt, self.validate)

    return super().format(record)
