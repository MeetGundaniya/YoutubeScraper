"""
Admin actions for ScraperApp
"""


# STDLIB LIBRARY
import logging
from datetime import datetime, timedelta

# DJANGO LIBRARY
from django.contrib import admin, messages
from django.utils.timezone import make_aware

# FIRSTPARTY LIBRARY
from core.helpers.async_http import Request
from core.models import Setting
from scraper.contrib import youtube
from scraper.models import Video, VideoMongo



logger = logging.getLogger(__name__)


@admin.action()
def get_channels_videos(modeladmin, request, queryset):
  """
  Create videos for each channel in the queryset
  """
  max_video = int(Setting.get_value('MAX_VIDEOS_FROM_CHANNEL'))

  for channel in queryset:

    try:
      logger.debug('extracting {}\'s videos', f'channel={channel}')
      url = 'https://www.youtube.com/'
      url += channel.custom_url or f'channel/{channel.channel_id}'
      

      records = []
      documents = []
      v_count = 0
      collection = {
        'records': [],
        'documents': [],
        'watch_reqs': [],
      }

      yc = youtube.Channel(url)
      existing_videos_id = [item[0] for item in channel.videos.values_list('video_id')]
      for v in filter(lambda _v: _v['id'] not in existing_videos_id, yc.video_generator()):

        try:
          video = Video(
            video_id=v['id'],
            title=v['title'],
            length= timedelta(**dict(zip(('hours', 'minutes', 'seconds'), map(int, v['length'].split(':'))))),
            view_count=v['view_count'],
            channel=channel,
          )
          m_video = VideoMongo(
            m_video=video,
            thumbnail_url=v['thumbnail_url'],
          )

        except KeyError as e:
          logger.warning('skipping video to add', exc_info=e)

        else:
          
          collection['records'].append(video)
          collection['documents'].append(m_video)

          yv = youtube.Video(f"https://www.youtube.com/watch?v={v['id']}")
          collection['watch_reqs'].append(yv._watch_payload())

          records.append(video)
          documents.append(m_video)

          v_count += 1
          if v_count >= max_video:
            break

      collection['watch_reqs'] = map(youtube.DataParser,  Request.results(collection['watch_reqs']))
      for parser,record,document in zip(collection['watch_reqs'], collection['records'], collection['documents'], strict=True):
        record.published_at = make_aware(datetime.strptime(parser['watch_result']['published_date'], '%b %d, %Y'))
        record.comment_count = parser['watch_result']['comment_count']
        record.like_count = parser['watch_result']['like_count']
        document.mv_description = parser['watch_result']['description']

      try:
        if records and documents:
          n = Video.objects.bulk_create(records, batch_size=20)
          m = VideoMongo.objects.bulk_create(documents, batch_size=20)
        else:
          n = m = []
      
      except Exception as e:
        logger.critical('unable to create video in bulk', exc_info=e)
      
      else:
        if len(n)!=len(m):
          logger.warning('{} videos of Video and {} of VideoMongo created, may break relationship', n, m)
        messages.add_message(request, messages.SUCCESS, f'new {len(n)} videos added')

    except Exception as e:
      logger.exception('failed to create {}\'s videos', f'channel={channel}', exc_info=e)

  logger.info('all videos created from selected channels queryset')
