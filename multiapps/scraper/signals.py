"""
This module processes the signal sent by the models of ScraperApp
"""

# STDLIB LIBRARY
import logging

# DJANGO LIBRARY
from django.db.models import signals
from django.dispatch.dispatcher import receiver

# FIRSTPARTY LIBRARY
from scraper.contrib import youtube
from scraper.models import Channel, ChannelMongo



logger = logging.getLogger(__name__)


@receiver(signals.pre_save, sender=Channel)
def pre_save_for_channel(sender, instance, *args, **kwargs):
  """
  Create channel instance on sql to store id, custom_url, title and subscriber
  """
  url = instance.custom_url or 'channel/' + instance.channel_id

  try:
    logger.debug('adding {} details', f'channel={instance}')
    yc = youtube.Channel(url=f'https://www.youtube.com/{url}')
    about = yc.about()
    
    instance.__detail = {
      'description': about['description'],
      'thumbnail_url': about['avatar'],
    }
    instance.channel_id = about['id']
    instance.custom_url = about['canonical_url'].split('.com/')[-1]
    instance.title = about['title']
    instance.subscriber = about['subscribers']

    logger.info('ready to add channel details on sql')

  except Exception as e:
    logger.exception('{} details not ready to add on sql', f'channel={instance}', exc_info=e)


@receiver(signals.post_save, sender=Channel)
def post_save_for_channel(sender, instance, created, *args, **kwargs):
  """
  Create channel instance on mongodb to store description and thumbnails
  """

  detail = instance.__detail
  del instance.__detail

  if created:
    try:
      logger.info(f'added channel details on sql')
      logger.debug('adding {} details to mongodb', f'channel={instance}')
      cm = ChannelMongo.objects.create(m_channel=instance, **detail)
      logger.info('added channel details on mongodb')
    except Exception as e:
      logger.exception('{} details not add on mongo', f'channel={instance}', exc_info=e)

  else:    
    try:
      logger.info(f'updated channel details on sql')
      logger.debug('updating {} details to mongodb', f'channel={instance}')
      cm = ChannelMongo.objects.get(m_channel=instance).update(**detail)
      logger.info('updated channel details on mongodb')
    except Exception as e:
      logger.exception('{} details not update on mongo', f'channel={instance}', exc_info=e)


@receiver(signals.pre_delete, sender=Channel)
def pre_delete_for_channel(sender, instance, *args, **kwargs):
  """
  Delete channel and associate document from mongo when channel deleted from sql
  """

  try:
    logger.debug('deleting {} related document from mongo', f'channel={instance}')
    ChannelMongo.objects.filter(m_channel=instance).delete()
    logger.info('channel related document deleted from mongo')

  except Exception as e:
    logger.exception('failed to delete {} related document from mongo', f'channel={instance}', exc_info=e)
