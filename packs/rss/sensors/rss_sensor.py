import calendar
import hashlib

import feedparser
from six.moves.html_parser import HTMLParser

from st2reactor.sensor.base import PollingSensor

__all__ = [
    'RSSSensor'
]


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


class RSSSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=None):
        super(RSSSensor, self).__init__(sensor_service=sensor_service,
                                        config=config,
                                        poll_interval=poll_interval)

        self._trigger_ref = 'rss.entry'
        self._logger = self._sensor_service.get_logger(__name__)

        config = self._config['sensor']
        self._use_published_at_filtering = config.get('use_published_at_filtering', True)

        # Stores a list of monitored feed urls
        self._feed_urls = {}

    def setup(self):
        pass

    def poll(self):
        feed_urls = self._feed_urls.keys()

        for feed_url in feed_urls:
            self._logger.info('Processing feed: %s' % (feed_url))
            processed_entries = self._process_feed(feed_url=feed_url)
            self._logger.info('Found and processed %s new entries for feed "%s"' %
                              (processed_entries, feed_url))

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        if trigger['type'] not in ['rss.feed']:
            return

        feed_url = trigger['parameters']['url']
        self._feed_urls[feed_url] = True

        self._logger.info('Added feed: %s', feed_url)

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        if trigger['type'] not in ['rss.feed']:
            return

        feed_url = trigger['parameters']['url']
        if feed_url in self._feed_urls:
            del self._feed_urls[feed_url]

        # TODO: Cleanup datastore for this feed
        self._logger.info('Removed feed: %s', feed_url)

    def _process_feed(self, feed_url):
        try:
            parsed = feedparser.parse(feed_url)
        except Exception:
            return

        feed = parsed['feed']
        entries = parsed.get('entries', [])

        # Retrieve timestamp of the last entry (if any)
        if self._use_published_at_filtering:
            last_published_at_ts = self._get_last_published_at(feed_url=feed_url)

        processed_entries_count = 0
        published_at_timestamps = []
        for entry in entries:
            published_at = entry.get('published_parsed', None)

            if self._use_published_at_filtering and published_at:
                published_at_ts = calendar.timegm(published_at)

                if published_at_ts <= last_published_at_ts:
                    # We have already seen this entry, skip it
                    continue

                published_at_timestamps.append(published_at_ts)

            self._dispatch_trigger_for_entry(feed=feed, entry=entry)
            processed_entries_count += 1

        # Store timestamp of the newest entry (if any)
        if self._use_published_at_filtering and published_at_timestamps:
            last_published_at_ts = max(published_at_timestamps)
            self._set_last_published_at(feed_url=feed_url, last_published_at=last_published_at_ts)

        return processed_entries_count

    def _get_last_published_at(self, feed_url):
        feed_id = hashlib.md5(feed_url).hexdigest()
        name = '%s.last_published_at' % (feed_id)
        last_published_at = self._sensor_service.get_value(name=name)

        if last_published_at:
            last_published_at = int(last_published_at)

        return last_published_at

    def _set_last_published_at(self, feed_url, last_published_at):
        feed_id = hashlib.md5(feed_url).hexdigest()
        name = '%s.last_published_at' % (feed_id)

        if last_published_at:
            self._sensor_service.set_value(name=name, value=str(last_published_at))

        return last_published_at

    def _dispatch_trigger_for_entry(self, feed, entry):
        trigger = self._trigger_ref

        feed_title = feed.get('title', None)
        feed_subtitle = feed.get('subtitle', None)
        feed_url = feed.get('link', None)
        feed_updated_at = feed.get('updated_parsed', None)

        if feed_updated_at:
            feed_updated_at = calendar.timegm(feed_updated_at)

        entry_title = entry.get('title', None)
        entry_author = entry.get('author', None)
        entry_published_at = entry.get('published_parsed', None)
        entry_summary = entry.get('summary', None)
        entry_content = entry.get('content', None)

        if entry_published_at:
            entry_published_at = calendar.timegm(entry_published_at)

        if entry_content:
            entry_content = entry_content[0].get('value', None)

            stripper = MLStripper()
            stripper.feed(entry_content)
            entry_content_raw = stripper.get_data()
        else:
            entry_content_raw = None

        payload = {
            'feed': {
                'title': feed_title,
                'subtitle': feed_subtitle,
                'url': feed_url,
                'feed_updated_at_timestamp': feed_updated_at
            },
            'entry': {
                'title': entry_title,
                'author': entry_author,
                'published_at_timestamp': entry_published_at,
                'summary': entry_summary,
                'content': entry_content,
                'content_raw': entry_content_raw
            }
        }

        self._sensor_service.dispatch(trigger=trigger, payload=payload)
