# pylint: disable=super-on-old-class
from operator import itemgetter
from urlparse import urljoin

import requests

from st2reactor.sensor.base import PollingSensor


class EventsConsumerSensor(PollingSensor):
    def __init__(self, sensor_service, config=None):
        super(EventsConsumerSensor, self).__init__(sensor_service=sensor_service,
                                                   config=config)
        self._trigger_ref = 'opscenter.event'

        self._logger = self._sensor_service.get_logger(__name__)
        self._base_url = self._config['opscenter_base_url']

        if not self._base_url.endswith('/'):
            self._base_url = self._base_url + '/'

        self._cluster_id = self.config['cluster_id']
        self._events_url = self._cluster_id + '/events'
        self._last_timestamp = None

    def setup(self):
        pass

    def poll(self):
        last_timestamp = self._get_last_timestamp()
        events = self._query_events(last_timestamp)

        if events:
            events.sort(key=itemgetter('timestamp'), reverse=True)
            last_timestamp = events[0]['timestamp']
            self._set_last_timestamp(last_timestamp)

            for event in events:
                self._dispatch_trigger_for_event(event=event)

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _query_events(self, timestamp=None, count_per_batch=50):
        params = {}
        params['count'] = count_per_batch
        params['reverse'] = '0'  # gets all newer events > timestamp.
        if timestamp:
            params['timestamp'] = timestamp

        all_events = []
        done = False
        while not done:
            events = requests.get(self._get_events_url(), params=params).json()
            all_events.extend(events)
            done = (len(events) < count_per_batch)

        return all_events

    def _get_events_url(self):
        return urljoin(self._base_url, self._events_url)

    def _get_last_timestamp(self):
        if not self._last_timestamp and hasattr(self._sensor_service, 'get_value'):
            self._last_timestamp = long(self._sensor_service.get_value(name='last_timestamp'))

        return self._last_timestamp

    def _set_last_timestamp(self, last_timestamp):
        self._last_timestamp = str(last_timestamp)

        if hasattr(self._sensor_service, 'set_value'):
            self._sensor_service.set_value(name='last_timestamp', value=last_timestamp)

    def _dispatch_trigger_for_event(self, event):
        trigger = self._trigger_ref
        payload = event
        self._sensor_service.dispatch(trigger=trigger, payload=payload)
