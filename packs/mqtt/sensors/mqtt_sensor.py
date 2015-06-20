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

        self._client = None
        self._hostname = self.config.get('hostname', None)
        self._port = self.config.get('port', 1883)
        self._client_id = self.config.get('client_id', None)
        self._userdata = self.config.get('userdata', None)
        self._username = self.config.get('username', None)
        self._password = self.config.get('password', None)
        self._subscribe = self.config.get('subscribe', None)
        self._ssl = self.config.get('ssl', False)
        self._ssl_cacert = self.config.get('ssl_cacert', None)
        self._ssl_cert = self.config.get('ssl_cert', None)
        self._ssl_key = self.config.get('ssl_key', None)

    def setup(self):
        self._client = mqtt.Client(self._client_id, clean_session=True,
                             userdata=self._userdata, protocol=MQTTv311)

        if self._username:
            self.client.username_pw_set(self._username, password=self._password)

        if self._ssl:
            if not self._ssl_cacert:
                raise ValueError('[mqtt_sensor]: Missing "ssl_cacert" \
                                    config option')

            if not self.self._ssl_cert:
                raise ValueError('[mqtt_sensor]: Missing "ssl_cert" \
                                    config option')

            if not self.self._ssl_key:
                raise ValueError('[mqtt_sensor]: Missing "ssl_key" \
                                    config option')

            self.client.tls_set(self._ssl_cacert, certfile=self._ssl_cert,
                                keyfile=self._ssl_key,
                                cert_reqs=ssl.CERT_REQUIRED,
                                tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)

        # Wire up the adapter with the appropriate callback methods
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message

        # Must be the last thing in the chain
        self._client.connect(self._host, port=self._port)

    def run(self):
        self._client.loop_forever()

    def cleanup(self):
        self._client.disconnect()

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _on_connect(client, userdata, flags, rc):
        self._logger.debug('[MQTTSensor]: Connected with result code '+str(rc))
        if self._subscribe:
            for topic in self.subscribe:
                self._logger.debug('[MQTTSensor]: Subscribing to '+str(topic))
                self._client.subscribe(topic)

    def _on_message(self, client, userdata, msg):
        self._logger.debug('[MQTTSensor] ({}) {}/{}'.format(client,
                                                            msg.topic,
                                                            str(msg.payload)))

        payload = {
            'client': client,
            'userdata': userdata,
            'message': msg,
        }
        self._sensor_service.dispatch(trigger=self._trigger, payload=message)
