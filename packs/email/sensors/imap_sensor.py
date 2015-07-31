import hashlib
import base64

import six
import eventlet
import easyimap
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

DEFAULT_DOWNLOAD_ATTACHMENTS = False
DEFAULT_MAX_ATTACHMENT_SIZE = 1024
DEFAULT_ATTACHMENT_DATASTORE_TTL = 1800


class IMAPSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=30):
        super(IMAPSensor, self).__init__(sensor_service=sensor_service,
                                         config=config,
                                         poll_interval=poll_interval)

        self._trigger = 'email.imap.message'
        self._logger = self._sensor_service.get_logger(__name__)

        self._max_attachment_size = self._config.get('max_attachment_size',
                                                     DEFAULT_MAX_ATTACHMENT_SIZE)
        self._attachment_datastore_ttl = self._config.get('attachment_datastore_ttl',
                                                          DEFAULT_MAX_ATTACHMENT_SIZE)
        self._mailboxes = {}

    def setup(self):
        self._logger.debug('[IMAPSensor]: entering setup')

    def poll(self):
        self._logger.debug('[IMAPSensor]: entering poll')

        if 'imap_mailboxes' in self._config:
            self._parse_mailboxes(self._config['imap_mailboxes'])

        for name, values in self._mailboxes.items():
            mailbox = values['connection']
            download_attachments = values['download_attachments']
            self._poll_for_unread_messages(name=name, mailbox=mailbox,
                                           download_attachments=download_attachments)
            mailbox.quit()

    def cleanup(self):
        self._logger.debug('[IMAPSensor]: entering cleanup')

        for name, values in self._mailboxes.items():
            mailbox = values['connection']
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
            server = config.get('server', 'localhost')
            port = config.get('port', 143)
            user = config.get('username', None)
            password = config.get('password', None)
            folder = config.get('mailbox', 'INBOX')
            ssl = config.get('ssl', False)
            download_attachments = config.get('download_attachments', DEFAULT_DOWNLOAD_ATTACHMENTS)

            if not user or not password:
                self._logger.debug("""[IMAPSensor]: Missing
                    username/password for {0}""".format(mailbox))
                continue

            if not server:
                self._logger.debug("""[IMAPSensor]: Missing server
                    for {0}""".format(mailbox))
                continue

            try:
                connection = easyimap.connect(server, user, password,
                                              folder, ssl=ssl, port=port)
            except Exception as e:
                message = 'Failed to connect to mailbox "%s": %s' % (mailbox, str(e))
                raise Exception(message)

            item = {
                'connection': connection,
                'download_attachments': download_attachments
            }
            self._mailboxes[mailbox] = item

    def _poll_for_unread_messages(self, name, mailbox, download_attachments=False):
        self._logger.debug('[IMAPSensor]: polling mailbox {0}'.format(name))

        messages = mailbox.unseen()

        self._logger.debug('[IMAPSensor]: Processing {0} new messages'.format(len(messages)))
        for message in messages:
            self._process_message(uid=message.uid, mailbox=mailbox,
                                  download_attachments=download_attachments)

    def _process_message(self, uid, mailbox, download_attachments=DEFAULT_DOWNLOAD_ATTACHMENTS):
        message = mailbox.mail(uid, include_raw=True)
        mime_msg = mime.from_string(message.raw)

        body = message.body
        sent_from = message.from_addr
        sent_to = message.to
        subject = message.title
        date = message.date
        message_id = message.message_id
        headers = mime_msg.headers.items()
        has_attachments = bool(message.attachments)

        # Flatten the headers so they can be unpickled
        headers = self._flattern_headers(headers=headers)

        payload = {
            'uid': uid,
            'from': sent_from,
            'to': sent_to,
            'headers': headers,
            'date': date,
            'subject': subject,
            'message_id': message_id,
            'body': body,
            'has_attachments': has_attachments,
            'attachments': []
        }

        if has_attachments and download_attachments:
            self._logger.debug('[IMAPSensor]: Downloading attachments for message {}'.format(uid))
            result = self._download_and_store_message_attachments(message=message)
            payload['attachments'] = result

        self._sensor_service.dispatch(trigger=self._trigger, payload=payload)

    def _download_and_store_message_attachments(self, message):
        """
        Method which downloads the provided message attachments and stores them in a datasatore.

        :rtype: ``list`` of ``dict``
        """
        attachments = message.attachments

        result = []
        for (file_name, content, content_type) in attachments:
            attachment_size = len(content)

            if len(content) > self._max_attachment_size:
                self._logger.debug(('[IMAPSensor]: Skipping attachment "{}" since its bigger '
                                    'than maximum allowed size ({})'.format(file_name,
                                                                            attachment_size)))
                continue

            datastore_key = self._get_attachment_datastore_key(message=message,
                                                               file_name=file_name)

            # Store attachment in the datastore
            if content_type == 'text/plain':
                value = content
            else:
                value = base64.b64encode(content)

            self._sensor_service.set_value(name=datastore_key, value=value,
                                           ttl=self._attachment_datastore_ttl,
                                           local=False)
            item = {
                'file_name': file_name,
                'content_type': content_type,
                'datastore_key': datastore_key
            }
            result.append(item)

        return result

    def _get_attachment_datastore_key(self, message, file_name):
        key = '%s-%s' % (message.uid, file_name)
        key = 'attachments-%s' % (hashlib.md5(key).hexdigest())
        return key

    def _flattern_headers(self, headers):
        # Flattern headers and make sure they only contain simple types so they
        # can be serialized in a trigger
        result = []

        for pair in headers:
            name = pair[0]
            value = pair[1]

            if not isinstance(value, six.string_types):
                value = str(value)

            result.append([name, value])

        return result
