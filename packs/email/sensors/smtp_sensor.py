import eventlet
import smtpd
from eventlet.green import asyncore
from flanker import mime

from st2reactor.sensor.base import Sensor

__all__ = [
    'SMTPSensor'
]

eventlet.monkey_patch(
    os=True,
    select=True,
    socket=True,
    thread=True,
    time=True)

class SMTPSensor(Sensor):
    def __init__(self, sensor_service, config=None):
        super(SMTPSensor, self).__init__(sensor_service=sensor_service,
                                         config=config)

        self._trigger = 'email.smtp.message'
        self._logger = self._sensor_service.get_logger(__name__)
        self._server = None
        self._listen_ip = self._config.get('smtp_listen_ip', '127.0.0.1')
        self._listen_port = self._config.get('smtp_listen_port', 25)

    def setup(self):
        self._logger.debug('[SMTPSensor]: entering setup')
        self._server = St2SMTPServer(localaddr=(self._listen_ip, self._listen_port),
                                     remoteaddr=None,
                                     sensor_service=self._sensor_service,
                                     logger=self._logger,
                                     trigger=self._trigger)

    def run(self):
        self._logger.debug('[SMTPSensor]: entering run')
        asyncore.loop()

    def cleanup(self):
        self._logger.debug('[SMTPSensor]: entering cleanup')

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

class St2SMTPServer(smtpd.SMTPServer):
    def __init__(self, localaddr, remoteaddr, sensor_service, logger, trigger):
        smtpd.SMTPServer.__init__(self, localaddr, remoteaddr)
        self._logger = logger
        self._trigger = trigger
        self._sensor_service = sensor_service

    def process_message(self, peer, mailfrom, rcpttos, data):
        self._logger.debug('posting message')

        message = mime.from_string(data)
        subject = message.subject()
        headers = json.dumps(message.header.items())
        body = message.parts.body

        payload = {
            'from': mailfrom,
            'to': rcpttos,
            'cc': None,
            'bcc': None,
            'subject': subject,
            'headers': headers,
            'body': body,
            'attachments': None
        }

        self._sensor_service.dispatch(trigger=self._trigger, payload=payload)
        return
