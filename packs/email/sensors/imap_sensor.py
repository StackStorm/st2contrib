import eventlet
import easyimap
import json
from flanker import mime

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
        self._mailboxes = {}

    def setup(self):
        self._logger.debug('[IMAPSensor]: entering setup')

        if 'imap_mailboxes' in self._config:
            self._parse_mailboxes(self._config['imap_mailboxes'])

    def poll(self):
        self._logger.debug('[IMAPSensor]: entering poll')

        for name, mailbox in self._mailboxes.items():
            self._poll_for_unread_messages(name, mailbox)

    def cleanup(self):
        self._logger.debug('[IMAPSensor]: entering cleanup')

        for name, mailbox in self._mailboxes.items():
            self._logger.debug('[IMAPSensor]: Disconnecting from {0}'.format(name))
            mailbox.quit()

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _parse_mailboxes(self, mailboxes):
        for mailbox, config in mailboxes.items():
            server   = config.get('server', 'localhost')
            port     = config.get('port', 143)
            user     = config.get('username', None)
            password = config.get('password', None)
            folder   = config.get('mailbox', 'INBOX')
            ssl      = config.get('ssl', False)

            if not user or not password:
                self._logger.debug('[IMAPSensor]: Missing username/password for {0}'.format(mailbox))
            elif not server:
                self._logger.debug('[IMAPSensor]: Missing server for {0}'.format(mailbox))
            else:
                connection = easyimap.connect(server, user, password, folder, ssl=ssl, port=port)
                self._mailboxes[mailbox] = connection

    def _poll_for_unread_messages(self, name, mailbox):
        self._logger.debug('[IMAPSensor]: polling mailbox {0}'.format(name))

        for message in mailbox.unseen():
            self._process_message(message.uid, mailbox)

    def _process_message(self, uid, mailbox):
        message = mailbox.mail(uid, include_raw=True)
        mime_msg = mime.from_string(message.raw)

        body = message.body
        sent_from = message.from_addr
        sent_to = message.to
        subject = message.title
        date = message.date
        message_id = message.message_id
        headers = mime_msg.headers.items()

        payload = {
            'uid': uid,
            'from': sent_from,
            'to': sent_to,
            'headers': headers,
            'date': date,
            'subject': subject,
            'message_id': message_id,
            'body': body,
            'attachments': None
        }

        self._sensor_service.dispatch(trigger=self._trigger, payload=payload)
