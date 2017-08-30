# Licensed to the StackStorm, Inc ('StackStorm') under one or more

# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import json

import eventlet
from flask import request, Flask

from st2reactor.sensor.base import Sensor
from st2common.util import isotime

__all__ = [
    'ServiceNotificationsSensor'
]

eventlet.monkey_patch(
    os=True,
    select=True,
    socket=True,
    thread=False if '--use-debugger' in sys.argv else True,
    time=True)


SUPPORTED_SERVICES_EVENT_KEYS = [
    's3'
]


class ServiceNotificationsSensor(Sensor):
    def __init__(self, sensor_service, config=None):
        super(ServiceNotificationsSensor, self).__init__(sensor_service=sensor_service,
                                                         config=config)
        self._config = self._config.get('service_notifications_sensor', {})

        self._host = self._config.get('host', 'localhost')
        self._port = self._config.get('port', 12345)
        self._path = self._config.get('path', None)

        if not self._path:
            raise ValueError('path setting not configured')

        self._log = self._sensor_service.get_logger(__name__)
        self._app = Flask(__name__)

    def setup(self):
        pass

    def run(self):
        @self._app.route(self._path, methods=['POST'])
        def handle_notification_webhook():
            return self._handle_notification_webhook()

        self._log.info('Listening for webhooks on http://%s:%s%s' %
                       (self._host, self._port, self._path))
        self._app.run(host=self._host, port=self._port)

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _handle_notification_webhook(self):
        self._log.debug('Received webhook, data=%s' % (request.data))

        try:
            data = json.loads(request.data)
        except ValueError as e:
            self._log.debug('Failed to parse body as JSON')
            return ''

        message = data.get('Message', None)

        if not message:
            self._log.debug('Payload contains no "Message attribute, skipping"')
            return ''

        try:
            message = json.loads(message)
        except ValueError as e:
            self._log.info('Failed to parse message as JSON: %s (message=%s)' %
                           (str(e), message))
            # log
            return ''

        self._process_message(message=message)
        return ''

    def _process_message(self, message):
        records = message.get('Records', [])

        for record in records:
            self._dispatch_trigger_for_record(record=record)

    def _dispatch_trigger_for_record(self, record):
        trigger = 'aws.service_notification'

        timestamp_datetime = isotime.parse(record['eventTime'])
        timestamp = int(timestamp_datetime.strftime('%s'))  # pylint: disable=no-member

        source = record.get('eventSource', 'unknown')
        region = record.get('awsRegion', 'unknown')
        name = record.get('eventName', 'unknown')
        request_parameters = record['requestParameters']
        response_elements = record['responseElements']

        # Build event specified payload object
        event_payload = None
        for event_key in SUPPORTED_SERVICES_EVENT_KEYS:
            value = record.get(event_key, None)
            if value:
                event_payload = value
                break

        if not event_payload:
            # Unsupported service
            return

        payload = {
            # Common attributes for all the AWS services events
            'source': source,
            'region': region,
            'name': name,
            'timestamp': timestamp,
            'request_parameters': request_parameters,
            'response_elements': response_elements,

            # Service and event specific payload
            'payload': event_payload
        }

        self._sensor_service.dispatch(trigger=trigger, payload=payload)
