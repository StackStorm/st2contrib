# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the 'License'); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from flask import Flask, request, abort
from st2reactor.sensor.base import Sensor

TRIGGER_REF = 'circle_ci.build_event'


class CircleCIWebhookSensor(Sensor):

    def setup(self):
        self.host = self._config['host']
        self.port = self._config['port']
        self._endpoints = self._config['endpoints']
        self.app = Flask(__name__)
        self.trigger_ref = TRIGGER_REF
        self.log = self._sensor_service.get_logger(__name__)

        @self.app.route('/status')
        def status():
            return json.dumps({'response': 'OK'})

        @self.app.route('/webhooks/<path:endpoint>', methods=['POST'])
        def build_events(endpoint):

            if endpoint not in self._endpoints:
                self.log.error('Ignoring unknown endpoint : %s', endpoint)
                abort(404)

            webhook_body = request.get_json()
            payload = {}
            payload['headers'] = self._get_headers_as_dict(request.headers)
            payload['body'] = webhook_body

            response = self._sensor_service.dispatch(self.trigger_ref, payload)
            self.log.debug(json.dumps(response))
            return json.dumps({'response': 'triggerposted'})

    def run(self):
        self.app.run(host=self.host, port=self.port, threaded=True)

    def cleanup(self):
        # This is called when the st2 system goes down. You can perform cleanup operations like
        # closing the connections to external system here.
        pass

    def _get_headers_as_dict(self, headers):
        headers_dict = {}
        for key, value in headers:
            headers_dict[key] = value
        return headers_dict

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass
