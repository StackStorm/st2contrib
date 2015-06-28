import eventlet

eventlet.monkey_patch(
    os=True,
    select=True,
    socket=True,
    thread=True,
    time=True)

from st2reactor.sensor.base import Sensor
import paho.mqtt.client as mqtt


class MQTTSensor(Sensor):
    def __init__(self, sensor_service, config=None):
        super(MQTTSensor, self).__init__(sensor_service=sensor_service,
                                         config=config)

        self._trigger = 'mqtt.message'
        self._logger = self._sensor_service.get_logger(__name__)

        self._client = None
        self._hostname = self._config.get('hostname', None)
        self._port = self._config.get('port', 1883)
        self._protocol = self._config.get('protocol', 'MQTTv311')
        self._client_id = self._config.get('client_id', None)
        self._userdata = self._config.get('userdata', None)
        self._username = self._config.get('username', None)
        self._password = self._config.get('password', None)
        self._subscribe = self._config.get('subscribe', None)
        self._ssl = self._config.get('ssl', False)
        self._ssl_cacert = self._config.get('ssl_cacert', None)
        self._ssl_cert = self._config.get('ssl_cert', None)
        self._ssl_key = self._config.get('ssl_key', None)

    def setup(self):
        self._logger.debug('[MQTTSensor]: setting up sensor...')

        self._client = mqtt.Client(self._client_id, clean_session=True,
                             userdata=self._userdata, protocol=self._protocol)

        if self._username:
            self._client.username_pw_set(self._username, password=self._password)

        if self._ssl:
            if not self._ssl_cacert:
                raise ValueError('[mqtt_sensor]: Missing "ssl_cacert" \
                                    config option')

            if not self._ssl_cert:
                raise ValueError('[mqtt_sensor]: Missing "ssl_cert" \
                                    config option')

            if not self._ssl_key:
                raise ValueError('[mqtt_sensor]: Missing "ssl_key" \
                                    config option')

            self._client.tls_set(self._ssl_cacert, certfile=self._ssl_cert,
                                keyfile=self._ssl_key)

        # Wire up the adapter with the appropriate callback methods
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message

        # Must be the last thing in the chain
        self._client.connect(self._hostname, port=self._port)

    def run(self):
        self._logger.debug('[MQTTSensor]: entering runloop')
        self._client.loop_forever()

    def cleanup(self):
        self._logger.debug('[MQTTSensor]: entering cleanup')
        self._client.disconnect()

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _on_connect(self, client, userdata, flags, rc):
        self._logger.debug('[MQTTSensor]: Connected with code {}' + str(rc))
        if self._subscribe:
            for topic in self._subscribe:
                self._logger.debug('[MQTTSensor]: Sub to ' + str(topic))
                self._client.subscribe(topic)

    def _on_message(self, client, userdata, msg):
        payload = {
            'userdata': userdata,
            'topic': msg.topic,
            'message': str(msg.payload),
            'retain': msg.retain,
            'qos': msg.qos,
        }
        self._sensor_service.dispatch(trigger=self._trigger, payload=payload)
