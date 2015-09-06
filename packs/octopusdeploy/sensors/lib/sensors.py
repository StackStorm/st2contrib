try:
    import requests
except ImportError:
    message = ('Missing "requests", please install it using pip:\n'
               'pip install requests')
    raise ImportError(message)

import json
import time

from st2reactor.sensor.base import PollingSensor

__all__ = [
    'OctopusDeploySensor',
]


class OctopusDeploySensor(PollingSensor):
    def __init__(self,
                 sensor_service,
                 config,
                 poll_interval,
                 trigger_ref,
                 store_key):
        super(OctopusDeploySensor, self).__init__(sensor_service=sensor_service,
                                                  config=config,
                                                  poll_interval=poll_interval)
        self.client = self._init_client()
        self._last_date = None
        self._trigger_ref = trigger_ref
        self._store_key = store_key

    def _init_client(self):
        api_key = self._config['api_key']
        host = self._config['host']
        port = self._config['port']
        return OctopusDeployClient(api_key=api_key, host=host, port=port)

    def _to_date(self, date_string):
        date_string = date_string.split('.')[0]
        return time.strptime(date_string, '%Y-%m-%dT%H:%M:%S')

    def _build_uri(self):
        # big assumption but it'll cover 99% case,
        # as octopus runs https by default
        start = "http://" if self.client.port is 80 else "https://"
        return start + self.client.host + ":" + str(self.client.port) + "/api/"

    def _get_last_date(self):
        self._last_date = self._sensor_service.get_value(name=self._store_key)
        if self._last_date is None:
            return None
        return time.strptime(self._last_date, '%Y-%m-%dT%H:%M:%S')

    def _set_last_date(self, last_date):
        self._last_date = time.strftime('%Y-%m-%dT%H:%M:%S', last_date)
        self._sensor_service.set_value(name=self._store_key,
                                       value=self._last_date)

    def _to_triggers(self, items):
        triggers = []
        for item in items:
            triggers.append(self._to_trigger(item))
        return triggers

    def _to_trigger(self, item):
        # Implement to copy fields
        pass

    def _dispatch_trigger_for_payload(self, trigger_payload):
        trigger = self._trigger_ref
        self._sensor_service.dispatch(trigger=trigger, payload=trigger_payload)

    def make_post_request(self, action, payload):
        response = requests.post(self._build_uri() + action,
                                 data=json.dumps(payload), verify=False,
                                 headers=self.client.headers)
        return response.json()

    def make_get_request(self, action):
        response = requests.get(self._build_uri() + action,
                                verify=False,
                                headers=self.client.headers)
        return response.json()

    def setup(self):
        pass

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass


class OctopusDeployClient(object):
    def __init__(self, api_key, host, port):
        self.api_key = api_key
        self.host = host
        self.port = port
        self.headers = {'X-Octopus-ApiKey': self.api_key,
                        'Content-type': 'application/json',
                        'Accept': 'text/plain'}
