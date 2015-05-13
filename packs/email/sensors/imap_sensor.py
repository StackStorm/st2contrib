import eventlet
import imbox
import json

from st2reactor.sensor.base import PollingSensor

__all__ = [
    'IMAPSensor'
]

eventlet.monkey_patch(
    os=True,
    select=True,
    socket=True,
    thread=True,
    time=True)

class IMAPSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=30):
        super(IMAPSensor, self).__init__(sensor_service=sensor_service,
                                         config=config,
					                     poll_interval=poll_interval)

        self._trigger = 'email.imap.message'
        self._logger = self._sensor_service.get_logger(__name__)

    def setup(self):
        server = self._config.get('imap_server', 'localhost')
        username = self._config['imap_username']
        password = self._config['imap_password']
        ssl = self._config['imap_ssl']

        self._mailbox = imbox.Imbox(server, username, password, ssl)

    def poll(self):
        unread_messages = self._mailbox.messages(unread=True)
        for uid, message in unread_messages:
            self._logger.debug('processing message %s' % uid)
            self._process_message(message)

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _process_message(self, message):
        self._logger.debug('posting message')

        headers = json.dump(message['headers'])
        body = json.dump(message['body'])
        sent_from = json.dump(message['sent_from'])
        sent_to = json.dump(message['sent_to'])
        subject = message['subject']

        payload = {
            'from': sent_from,
            'to': sent_to,
            'cc': None,
            'bcc': None,
            'subject': subject,
            'headers': headers,
            'body': body,
            'attachments': None
        }

        self._sensor_service.dispatch(trigger=self._trigger, payload=payload)

