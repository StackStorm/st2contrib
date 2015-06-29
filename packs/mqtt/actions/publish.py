from st2actions.runners.pythonrunner import Action
import paho.mqtt.publish as publish


class PublishAction(Action):
    def __init__(self, config):
        super(PublishAction, self).__init__(config)

        # Sensor/Action Mismatch
        self._config = self.config

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

        self._ssl_payload = None
        self._auth_payload = None

    def run(self, topic, message=None, qos=0, retain=False):
        if self._username:
            self._auth_payload = {
                'username': self._username,
                'password': self._password,
            }

        if self._ssl:
            if not self._ssl_cacert:
                raise ValueError('Missing "ssl_cacert" config option')

            if not self._ssl_cert:
                raise ValueError('Missing "ssl_cert" config option')

            if not self._ssl_key:
                raise ValueError('Missing "ssl_key" config option')

            self._ssl_payload = {
                'ca_certs': self._ssl_cacert,
                'certfile': self._ssl_cert,
                'keyfile': self._ssl_key,
            }

        publish.single(topic, payload=message, qos=qos, retain=retain,
                       hostname=self._hostname, port=self._port,
                       client_id=self._client_id, keepalive=60,
                       auth=self._auth_payload, tls=self._ssl_payload,
                       protocol=self._protocol)
