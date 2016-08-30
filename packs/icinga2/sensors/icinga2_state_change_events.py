#!/usr/bin/env python

from lib.client import Client
from st2reactor.sensor.base import Sensor


class Icinga2StateChangeSensor(Sensor):
    def setup(self):
        self.logger = self._sensor_service.get_logger(__name__)
        self.api_url = self._config['api_url'] + '/events?queue=state_change&types=StateChange'
        self.api_user = self._config['api_state_change_user']
        self.api_password = self._config['api_state_change_password']
        self.trigger_name = 'event.state_change'
        self.trigger_pack = 'icinga2'
        self.trigger_ref = '.'.join([self.trigger_pack, self.trigger_name])
        self.client = Client(self, self.api_url, self.api_user, self.api_password)
        self.logger.info(
            'Icinga2StateChangeSensor initialized with URL: %s User: %s Password: *****',
            self.api_url, self.api_user)

    def process_event(self, event):
        self.logger.info('Processing event: %s', event)
        payload = {}
        payload['service'] = event['service']
        payload['host'] = event['host']
        payload['state'] = event['state']
        payload['state_type'] = event['state_type']
        payload['type'] = event['type']
        payload['check_result'] = event['check_result']
        self.dispatch_trigger(payload)

    def run(self):
        self.logger.info('Setting up API connection params.')
        self.client.setup_connection()
        self.logger.info('Starting connection to API endpoint.')
        self.client.start()

    def cleanup(self):
        self.client.abort_session()

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        self.client.abort_session()

    def dispatch_trigger(self, payload):
        self.logger.info('Dispatching trigger: %s', self.trigger_ref)
        self._sensor_service.dispatch(self.trigger_ref, payload)
