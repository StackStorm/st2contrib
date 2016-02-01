from st2reactor.sensor.base import Sensor
from signalr import Connection

__all__ = [
    'SignalRHubSensor'
]


class SignalRHubSensor(Sensor):
    def __init__(self, sensor_service, config=None):
        super(SignalRHubSensor, self).__init__(sensor_service=sensor_service,
                                               config=config)
        self._logger = self._sensor_service.get_logger(__name__)
        self.url = config['hub_url']
        self.hub_name = config['hub_name']
        self._trigger_ref = 'signalr.message_received'
        self._hub = None
        self.connection = None
        self.session = None

    def setup(self):
        self.connection = Connection(self.url, self.session)
        # start a connection
        self.connection.start()
        # add a handler to process notifications to the connection
        self.connection.handlers += \
            lambda data: self._logger.debug(
                'Connection: new notification - %s' % data)
        # get hub
        self._hub = self.connection.hub(self.hub_name)

    def message_received(self, message):
        self._logger.debug('Connection: new notification.' % message)
        self._sensor_service.dispatch(trigger=self._trigger_ref,
                                      payload={message: message})

    def run(self):
        self._hub.client.on('message_received',
                            SignalRHubSensor.message_received)

    def cleanup(self):
        # do not receive new messages
        self._hub.client.off('message_received', self.message_received)
        self.connection.close()
