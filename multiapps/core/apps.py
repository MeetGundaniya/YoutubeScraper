"""
Configuration for specific core app
"""

# STDLIB LIBRARY
import logging

# DJANGO LIBRARY
from django.apps import AppConfig
from django.db.models.signals import post_migrate



logger = logging.getLogger(__name__)


class CoreConfig(AppConfig):
  """
  Config for core app
  """
  logger = logging.LoggerAdapter(logger)

  default_auto_field = 'django.db.models.BigAutoField'
  name = 'core'

  def ready(self):
    self.logger.info('core is now ready')

    # FIRSTPARTY LIBRARY
    from core.signals import load_app_config_from_fixture
    post_migrate.connect(load_app_config_from_fixture, sender=self)

    try:
      self.get_model('setting').cache_values()
    except Exception as e:
      pass
