"""
Configuration for specific ScraperApp
"""

# STDLIB LIBRARY
import logging

# DJANGO LIBRARY
from django.apps import AppConfig



logger = logging.getLogger(__name__)


class ScraperConfig(AppConfig):
  """
  Config for scraper app
  """
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'scraper'

  def ready(self):
    logger.info('scraper is now ready')

    # FIRSTPARTY LIBRARY
    import scraper.signals
