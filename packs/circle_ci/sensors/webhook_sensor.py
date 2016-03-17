from st2reactor.sensor.base import Sensor
from flask import Flask, request, jsonify, abort, make_response
import json, requests


class CircleCIWebhookSensor(Sensor):

    def setup(self):
        self.host = self._config['host']
        self.port = self._config['port']
        self._endpoints = self._config['endpoints']
        self.app = Flask(__name__)
        self.trigger_ref = "circle_ci.build_event"
        self.log = self._sensor_service.get_logger(__name__)

        @self.app.route('/status')
        def status():
            return json.dumps({"response":"OK"})

        @self.app.route('/webhooks/<path:endpoint>', methods=['POST',])
        def build_events(endpoint):

            webhook_body = request.get_json()
            payload = {}
            payload['headers'] = self._get_headers_as_dict(request.headers)
            payload['body'] = webhook_body

            response = self._sensor_service.dispatch(self.trigger_ref, payload)
            self.log.info(json.dumps(response))
            return json.dumps({"response":"triggerposted"})

    def run(self):
        self.app.run(host=self.host,port=self.port,debug=True, threaded=True)

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
        self.remove_trigger(trigger)
        self.add_trigger(trigger)

    def remove_trigger(self, trigger):
        id = trigger['id']

        try:
            job_id = self._jobs[id]
        except KeyError:
            self._log.info('Job not found: %s', id)
            return

        self._scheduler.remove_job(job_id)

    def _get_trigger_type(self, ref):
        pass