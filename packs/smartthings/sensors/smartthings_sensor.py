import eventlet
import json
from flask import request, json, Flask, Response  # noqa
from st2reactor.sensor.base import Sensor

eventlet.monkey_patch(
    os=True,
    select=True,
    socket=True,
    thread=True,
    time=True)


class SmartThingsSensor(Sensor):
    def __init__(self, sensor_service, config=None):
        super(SmartThingsSensor, self).__init__(sensor_service=sensor_service,
                                                config=config)

        self._trigger = 'smartthings.event'
        self._logger = self._sensor_service.get_logger(__name__)

        self._listen_ip = self._config.get('listen_ip', '0.0.0.0')
        self._listen_port = self._config.get('listen_port', '12000')
        self._api_key = self._config.get('api_key', None)

        self._app = Flask(__name__)

    def setup(self):
        pass

    def run(self):
        if not self._api_key:
            raise Exception('[smartthings_sensor]: api_key config option not set')

        # Routes
        @self._app.route('/', methods=['PUT'])
        def process_incoming():
            response = None
            if request.headers['X-Api-Key'] == self._api_key:
                status = self._process_request(request)
                response = Response(status[0], status=status[1])
            else:
                response = Response('fail', status=401)

            return response

        # Start the Flask App
        self._app.run(host=self._listen_ip, port=self._listen_port)

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _process_request(self, request):
        if request.headers['Content-Type'] == 'application/json':
            payload = request.json
            self._logger.debug('[smartthings_sensor]: processing request {}'.format(payload))

            self._sensor_service.dispatch(trigger=self._trigger, payload=payload)
            return ('ok', 200)
        else:
            return ('fail', 415)
