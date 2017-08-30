from st2reactor.sensor.base import Sensor
from flask import Flask, request
import json


WEBHOOK_TRIGGER_REF = "activecampaign.webhook"


class ActiveCampaignWebhook(Sensor):
    """
    Receives webhooks from ActiveCampaign. Implemented as standalone
    to be run on DMZ.

    * self._sensor_service
        - provides utilities like
            - get_logger() - returns logger instance specific to this sensor.
            - dispatch() for dispatching triggers into the system.
    * self._config
        - contains parsed configuration that was specified as
          config.yaml in the pack.
    """

    def setup(self):
        self.host = self._config['webhook']['host']
        self.port = self._config['webhook']['port']
        path = self._config['webhook']['path']
        route = '/{}/{}'.format(path, '<string:action>')

        self.app = Flask(__name__)
        self.log = self._sensor_service.get_logger(__name__)

        @self.app.route('/status')
        def status():
            return json.dumps({"response": "OK"})

        @self.app.route(route, methods=['POST'])
        def ac_events(action):

            payload = {}
            payload['headers'] = self._get_headers_as_dict(request.headers)
            payload['body'] = request.form.to_dict(flat=True)
            payload['action'] = action

            self._sensor_service.dispatch(WEBHOOK_TRIGGER_REF, payload)
            return json.dumps({"response": "triggerposted"})

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=True)

    def cleanup(self):
        # This is called when the st2 system goes down.
        pass

    def add_trigger(self, trigger):
        # This method is called when trigger is created
        pass

    def update_trigger(self, trigger):
        # This method is called when trigger is updated
        pass

    def remove_trigger(self, trigger):
        # This method is called when trigger is deleted
        pass

    def _get_headers_as_dict(self, headers):
        headers_dict = {}
        for key, value in headers:
            headers_dict[key] = value
        return headers_dict
