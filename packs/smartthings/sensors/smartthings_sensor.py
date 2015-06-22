import eventlet
import json
from flask import json, Flask

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

        self._listen_ip = self._config.get('listen_ip', '0.0.0.0')
        self._listen_port = self._config.get('listen_port', '12000')
        self._api_key = self._config.get('api_key', None)

        self._trigger = 'smartthings.event'
        self._app = Flask(__name__)

    def setup(self):
        pass

    def run(self):
        if not self._api_key:
            raise Exception('[smartthings_sensor]: api_key config option not set')

        @self._app.route('/', methods=['POST'])
        def process_incoming():
            if request.headers['X-Api-Key'] == self._api_key:
                return self._process_request(request)
            else:
                abort(401)

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
            payload = json.dumps(request.json)
            self._sensor_service.dispatch(trigger=self._trigger, payload=payload)
        else:
            return "415 Unsupported Media Type"
