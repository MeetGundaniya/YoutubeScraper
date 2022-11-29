"""
Youtube http response parser
"""

# STDLIB LIBRARY
import json
import re
from contextlib import suppress



class DataParser:
  """
  Parse ytInitialData from youtube http response
  """
  def __getitem__(self, key):
    return self._parsed_data[key]

  def __contains__(self, key):
    return key in self._parsed_data.keys()

  def _parse_html(self, html):
    if not isinstance(html, str):
      return {}

    if html.startswith('<!DOCTYPE html>'):
      pattern = r'<script nonce=".{22}">var ytInitialData = .*;</script>'
      match = re.compile(pattern).search(html)

      if match is None:
        return {}

      return json.loads(match.string[match.start()+59:match.end()-10])
    return json.loads(html)

  def __init__(self, html=None, initial=None):
    self._parsed_data = initial._parsed_data if isinstance(initial, self.__class__) else {}
    self.initial = self._parse_html(html) or {}

    match self.initial:
      case {'contents': {'twoColumnBrowseResultsRenderer': {'tabs': tab_list}}, 'header': {'c4TabbedHeaderRenderer': tabbed_header}}:
        self._tabsRenderer(tab_list)
        self._tabbedHeaderRenderer(tabbed_header)
      case {'contents': {'twoColumnWatchNextResults': {'results': {'results': {'contents': results}}}}}:
        self._watchResultRenderer(results)
      case {'contents': {'twoColumnSearchResultsRenderer': {'primaryContents': {'sectionListRenderer': {'contents': section_list}}}}}:
        self._sectionListRenderer(section_list)
      case {'onResponseReceivedCommands': onResponseReceived}:
        self._sectionListRenderer(onResponseReceived[0]['appendContinuationItemsAction']['continuationItems'])
      case {'onResponseReceivedEndpoints': [_, {'reloadContinuationItemsCommand': {'continuationItems': comment_threads}}]}:
        self._commentThreadRenderer(comment_threads)

  def _tabbedHeaderRenderer(self, tabbed_header):
    self._parsed_data.setdefault('channelAboutRenderer', {}).update({
      'subscribers': tabbed_header['subscriberCountText']['simpleText'].split(' ')[0]
    })    

  def _commentThreadRenderer(self, comment_threads):
    context = self._parsed_data.setdefault('watch_result', {})   #{'channel': {}})
    context = context.setdefault('comments', [])
    for comment in comment_threads:
      match comment:
        case {'commentThreadRenderer': {'comment': {'commentRenderer': comment_renderer}}}:
          context.append(self.commentRenderer(comment_renderer))
        case {'continuationItemRenderer': continuation_item}:
          self._parsed_data['continuation'] = self.continuationItemRenderer(continuation_item)

  def commentRenderer(self, comment_renderer):
    context = {'author': {}}

    context['author']['id'] = comment_renderer['authorEndpoint']['browseEndpoint']['browseId']
    context['author']['title'] = comment_renderer['authorText']['simpleText']
    context['author']['thumbnail_url'] = comment_renderer['authorThumbnail']['thumbnails'][-1]['url']
    context['id'] = comment_renderer['commentId']
    context['text'] = '\n'.join(run['text'] for run in comment_renderer['contentText']['runs'])
    context['relative_published_date'] = comment_renderer['publishedTimeText']['runs'][-1]['text']

    try:
      context['vote_count'] = comment_renderer['voteCount']['simpleText']
    except KeyError:
      context['vote_count'] = '0'

    return context
    
  def _watchResultRenderer(self, results):
    context = self._parsed_data.setdefault('watch_result', {})

    for result in results:
      match result:
        case {'videoPrimaryInfoRenderer': primary_info}:
          context['published_date'] = primary_info['dateText']['simpleText']
          context['relative_published_date'] = primary_info['relativeDateText']['simpleText']
          context['title'] = primary_info['title']['runs'][0]['text']
          context['short_view_count'] = primary_info['viewCount']['videoViewCountRenderer']['shortViewCount']['simpleText']
          context['view_count'] = primary_info['viewCount']['videoViewCountRenderer']['viewCount']['simpleText']
          context['like_count'] = primary_info['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer']['likeButton']['toggleButtonRenderer']['defaultText']['simpleText']

        case {'videoSecondaryInfoRenderer': secondary_info}:
          try:
            context['description'] = '\n'.join(run['text'] for run in secondary_info['description']['runs'])
          except KeyError:
            context['description'] = secondary_info['attributedDescription']['content']

          context['channel'] = {
            'subscriber': secondary_info['owner']['videoOwnerRenderer']['subscriberCountText']['simpleText'],
            'thumbnail': secondary_info['owner']['videoOwnerRenderer']['thumbnail']['thumbnails'][-1]['url'],
            'title': secondary_info['owner']['videoOwnerRenderer']['title']['runs'][0]['text'],
          }

        case {'itemSectionRenderer': {'contents': item_section_list}}:
          self._itemSectionRenderer(item_section_list)

  def _tabsRenderer(self, tabs):
    for tab in tabs:
      match tab:
        case {'tabRenderer': {'title': 'Home', 'content': data}}:
          pass
        case {'tabRenderer': {'title': 'Videos', 'content': {'richGridRenderer': {'contents': rich_grid_list, 'header': {'feedFilterChipBarRenderer': {'contents': feed_filter_list}}}}}}:
          self._richGridRenderer(rich_grid_list)
          self._chipCloudChipRenderer(feed_filter_list)
        case {'tabRenderer': {'title': 'Shorts', 'content': data}}:
          pass
        case {'tabRenderer': {'title': 'Live', 'content': data}}:
          pass
        case {'tabRenderer': {'title': 'Playlists', 'content': data}}:
          pass
        case {'tabRenderer': {'title': 'Community', 'content': data}}:
          pass
        case {'tabRenderer': {'title': 'Channels', 'content': data}}:
          pass
        case {'tabRenderer': {'title': 'About', 'content': {'sectionListRenderer': {'contents': section_list}}}}:
          self._sectionListRenderer(section_list)
        case {'tabRenderer': {'title': 'Search', 'content': data}}:
          pass

  def _richGridRenderer(self, rich_grids):
    for rich_item in rich_grids:
      match rich_item:
        case {'richItemRenderer': {'content': {'videoRenderer': video_renderer}}}:
          self._parsed_data.setdefault('videoRenderer', []).append(self.videoRenderer(video_renderer))
        case {'continuationItemRenderer': continuation_item}:
          self._parsed_data['continuation'] = self.continuationItemRenderer(continuation_item)

  def _sectionListRenderer(self, sections):
    for section in sections:
      match section:
        case {'itemSectionRenderer': {'contents': item_section_list}}:
          self._itemSectionRenderer(item_section_list)
        case {'continuationItemRenderer': continuation_item}:
          self._parsed_data['continuation'] = self.continuationItemRenderer(continuation_item)

  def _itemSectionRenderer(self, item_sections):
    for content in item_sections:
      match content:
        case {'searchPyvRenderer': search_renderer}:
          pass
        case {'channelRenderer': channel_renderer}:
          self._parsed_data.setdefault('channelRenderer', []).append(channel_renderer)
        case {'videoRenderer': video_renderer}:
          with suppress(KeyError):
            self._parsed_data.setdefault('videoRenderer', []).append(self.videoRenderer(video_renderer))
        case {'shelfRenderer': shelf_renderer}:
          with suppress(KeyError):
            self._parsed_data.setdefault('shelfRenderer', []).append(self.shelfRenderer(shelf_renderer))
        case {'playlistRenderer': playlist_renderer}:
          self._parsed_data.setdefault('playlistRenderer', []).append(playlist_renderer)
        case {'radioRenderer': radio_renderer}:
          self._parsed_data.setdefault('radioRenderer', []).append(radio_renderer)
        case {'channelAboutFullMetadataRenderer': channel_about}:
          self._parsed_data.setdefault('channelAboutRenderer', {}).update(self.channelAboutRenderer(channel_about))
        case {'commentsEntryPointHeaderRenderer': {'commentCount': {'simpleText': comment_count}}}:
          self._parsed_data.setdefault('watch_result', {})['comment_count'] = comment_count
        case {'continuationItemRenderer': continuation_item}:
          self._parsed_data['continuation'] = self.continuationItemRenderer(continuation_item)

  def continuationItemRenderer(self, continuation_item):
    return {
      'trigger': continuation_item['trigger'],
      'token': continuation_item['continuationEndpoint']['continuationCommand']['token'],
      'request': continuation_item['continuationEndpoint']['continuationCommand']['request'],
    }

  def shelfRenderer(self, shelf_renderer):
    category = shelf_renderer['title']['simpleText']
    for video_renderer in shelf_renderer['content']['verticalListRenderer']['items']:
      yield self.videoRenderer(video_renderer['videoRenderer'])

  def videoRenderer(self, video_renderer):
    contexts = {}

    contexts['id'] = video_renderer['videoId']
    contexts['title'] = video_renderer['title']['runs'][0]['text']

    if 'viewCountText' in video_renderer:
      if 'runs' in video_renderer['viewCountText']:
        view_count_text = video_renderer['viewCountText']['runs'][0]['text']
      else:
        view_count_text = video_renderer['viewCountText']['simpleText']
      stripped_text = view_count_text.split()[0].replace(',','')
      contexts['view_count'] = 0 if stripped_text=='No' else int(stripped_text)
    else:
      contexts['view_count'] = 0

    if 'lengthText' in video_renderer:
      contexts['length'] = video_renderer['lengthText']['simpleText']
    else:
      contexts['length'] = 0

    contexts['thumbnail_url'] = video_renderer['thumbnail']['thumbnails'][-1]['url']
    contexts['published_at'] = video_renderer['publishedTimeText']['simpleText']

    with suppress(KeyError):
      contexts['moving_thumbnail_url'] = video_renderer['richThumbnail']['movingThumbnailRenderer']['movingThumbnailDetails']['thumbnails'][0]['url']
      contexts['description'] = video_renderer['descriptionSnippet']['runs'][0]['text']
      contexts['published_at'] = video_renderer['publishedTimeText']['runs'][0]['text']
    
    with suppress(KeyError):
      contexts['channel'] = {
        'id': video_renderer['ownerText']['runs'][0]['navigationEndpoint']['browseEndpoint']['browseId'],
        'canonical_url': video_renderer['ownerText']['runs'][0]['navigationEndpoint']['browseEndpoint']['canonicalBaseUrl'],
        'title': video_renderer['ownerText']['runs'][0]['text'],
        'thumbnail_url': video_renderer['channelThumbnailSupportedRenderers']['channelThumbnailWithLinkRenderer']['thumbnail']['thumbnails'][-1]['url'],
      }

    return contexts

  def channelAboutRenderer(self, channel_about):
    contexts = {}

    contexts['avatar'] = channel_about['avatar']['thumbnails'][-1]['url']
    contexts['canonical_url'] = channel_about['canonicalChannelUrl']
    contexts['id'] = channel_about['channelId']
    contexts['country'] = channel_about['country']['simpleText']
    contexts['description'] = channel_about['description']['simpleText']
    contexts['joined'] = channel_about['joinedDateText']['runs'][1]['text']
    # contexts['primaryLinks']         # Implemented when it require
    contexts['title'] = channel_about['title']['simpleText']
    contexts['view_count'] = channel_about['viewCountText']['simpleText']

    return contexts

  def _chipCloudChipRenderer(self, feed_filters):
    contexts = {
      'selected_feed': None,
      'feeds': [],
    }

    for feed in feed_filters:
      contexts['feeds'].append(feed['chipCloudChipRenderer']['text']['simpleText'])
      if feed['chipCloudChipRenderer']['isSelected']:
        contexts['selected_feed'] = contexts['feeds'][-1]
    return contexts
