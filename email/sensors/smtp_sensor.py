#       - from
#       - to
#       - cc
#       - bcc
#       - headers
#       - subject
#       - body
#       - attachments
import eventlet
import asyncore
import smtpd
from flanker import mime

from st2reactor.sensor.base import PollingSensor

__all__ = [
    'SMTPSensor'
]

eventlet.monkey_patch(
    os=True,
    select=True,
    socket=True,
    thread=True,
    time=True)

class SMTPSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=1):
        super(SMTPSensor, self).__init__(sensor_service=sensor_service,
                                         config=config,
					 poll_interval=poll_interval)

        self._trigger = 'email.message'
        self._logger = self._sensor_service.get_logger(__name__)

    def setup(self):
        self._server = St2SMTPServer(localaddr=('127.0.0.1', 25),
                                     remoteaddr=None,
                                     sensor_service=self._sensor_service,
                                     logger=self._logger,
                                     trigger=self._trigger)

    def poll(self):
        asyncore.loop()

    def cleanup(self):
        pass

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
