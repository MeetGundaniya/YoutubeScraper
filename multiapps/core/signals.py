"""
This module processes the signal sent by the model
"""

# STDLIB LIBRARY
import logging

# DJANGO LIBRARY
from django.core.management import call_command



logger = logging.getLogger(__name__)


def load_app_config_from_fixture(sender, *args, **kwargs):
  """
  Call once when app's models was migrated
  """
  try:
    call_command('loaddata', 'db_backup_setting.json')
    logger.info('app level setting loaded from fixture')
  except Exception as e:
    logger.warning('failed to load app level setting from fixture due to {}', f'{e}')
