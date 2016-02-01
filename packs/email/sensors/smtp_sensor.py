import eventlet

eventlet.monkey_patch(
    os=True,
    select=True,
    socket=True,
    thread=True,
    time=True)

from eventlet.green import asyncore
import smtpd_green as smtpd
from flanker import mime
import hashlib
import base64

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
        asyncore.loop()  # pylint: disable=no-member

    def cleanup(self):
        self._logger.debug('[SMTPSensor]: entering cleanup')

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass


class St2SMTPServer(smtpd.SMTPServer):  # pylint: disable=no-member
    def __init__(self, localaddr, remoteaddr, sensor_service, logger, trigger):
        smtpd.SMTPServer.__init__(self, localaddr, remoteaddr)  # pylint: disable=no-member
        self._logger = logger
        self._trigger = trigger
        self._sensor_service = sensor_service

    def process_message(self, peer, mailfrom, rcpttos, data):
        self._logger.debug('posting message from {} to {}'.format(mailfrom, rcpttos))

        message = self.parse_message(mailfrom, rcpttos, data)
        self._sensor_service.dispatch(trigger=self._trigger, payload=message)
        return

    def parse_message(self, mailfrom, rcpttos, data):
        message = mime.from_string(data)
        payload = {
            'from': None,
            'to': None,
            'subject': None,
            'date': None,
            'body_plain': None,
            'body_html': None,
            'attachments': [],
            'headers': message.headers.items(),
        }

        # Try to get the addressee via headers, or
        # fall-back to raw protocol request
        if 'To' in message.headers.keys():
            payload['to'] = message.headers['To']
        else:
            payload['to'] = rcpttos

        # Try to get the recipient via headers, or
        # fall-back to raw protocol request
        if 'From' in message.headers.keys():
            payload['from'] = message.headers['From']
        else:
            payload['from'] = mailfrom

        if 'Subject' in message.headers.keys():
            payload['subject'] = message.headers['Subject']

        if 'Date' in message.headers.keys():
            payload['date'] = message.headers['Date']

        # Body
        if message.content_type.is_singlepart():
            payload['body_plain'] = message.body
        elif message.content_type.is_multipart():
            for part in message.parts:
                content_type = part.content_type[0]

                if content_type == 'text/plain':
                    payload['body_plain'] = part.body
                elif content_type == 'text/html':
                    payload['body_html'] = part.body
                elif part.is_attachment():
                    attachment = {
                        'filename': part.detected_file_name,
                        'md5': hashlib.md5(part.body).hexdigest(),
                        'sha1': hashlib.sha1(part.body).hexdigest(),
                        'data': base64.b64encode(part.body),
                        'encoding': part.content_encoding[0],
                        'type': content_type,
                    }
                    payload['attachments'].append(attachment)

        return payload
