import eventlet

eventlet.monkey_patch(
    os=True,
    select=True,
    socket=True,
    thread=True,
    time=True)

from eventlet.green import asyncore
import json
import smtpd_green as smtpd
from flanker import mime

from st2reactor.sensor.base import Sensor

class SMTPSensor(Sensor):
    def __init__(self, sensor_service, config=None):
        super(SMTPSensor, self).__init__(sensor_service=sensor_service,
                                         config=config)

        self._trigger = 'email.smtp.message'
        self._logger = self._sensor_service.get_logger(__name__)
        self._server = None
        self._listen_ip = self._config.get('smtp_listen_ip', '127.0.0.1')
        self._listen_port = self._config.get('smtp_listen_port', 1025)

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
        self._logger.debug('posting message from {0} to {1}'.format(mailfrom, rcpttos))

        # message = mime.from_string(data)
        # subject = message.subject()
        # headers = json.dumps(message.header.items())
        # body = message.parts.body

        payload = {
            'from': None,
            'to': None,
            'cc': None,
            'bcc': None,
            'subject': None,
            'headers': None,
            'body': None,
            'attachments': None
        }

        self._sensor_service.dispatch(trigger=self._trigger, payload=payload)
        return
