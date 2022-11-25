"""
Controlling which model should be contained in which database
"""

# STDLIB LIBRARY
import logging

# DJANGO LIBRARY
from django.db.utils import ConnectionRouter



logger = logging.getLogger(__name__)


class ScraperRouter(ConnectionRouter):
  """
  A router to control database operations on models
  """

  logger = logging.LoggerAdapter(logger)


  def db_for_read(self, model, **hints):
    """
    Attempts to read data for model from database.
    """
    
    db = getattr(model, '_database', {}).get('using', 'default')
    model_name = model._meta.db_table
    self.logger.debug('accessing {} for {}', f'{db=}', f'{model_name=}')
    return db

  def db_for_write(self, model, **hints):
    """
    Attempts to write data for model in database.
    """

    db = getattr(model, '_database', {}).get('using', 'default')
    model_name = model._meta.db_table
    self.logger.debug('accessing {} for {}', f'{db=}', f'{model_name=}')
    return db

  def allow_relation(self, obj1, obj2, **hints):
    """
    Attempts to make relation between models which comes from different database.
    """

    self.logger.debug('allow model relation between {} and {}', f'{obj1}', f'{obj2}')
    return True

  def allow_migrate(self, db, app_label, model_name=None, **hints):
    """
    Attempts to migrate models in database.
    """

    if app_label in ('core', 'scraper'):
      match db:
        case 'default':
          rtn = True
        case 'mongodb':
          rtn = False
    else:
      rtn = None
    
    self.logger.debug('{} for {} and {}', f'{rtn=}', f'{db=}', f'{app_label=}')
    return rtn
