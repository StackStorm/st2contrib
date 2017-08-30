import json
import re

import eventlet
from slackclient import SlackClient

from st2reactor.sensor.base import PollingSensor

eventlet.monkey_patch(
    os=True,
    select=True,
    socket=True,
    thread=True,
    time=True)

EVENT_TYPE_WHITELIST = [
    'message'
]


class SlackSensor(PollingSensor):
    DATASTORE_KEY_NAME = 'last_message_timestamp'

    def __init__(self, sensor_service, config=None, poll_interval=None):
        super(SlackSensor, self).__init__(sensor_service=sensor_service,
                                          config=config,
                                          poll_interval=poll_interval)
        self._logger = self._sensor_service.get_logger(__name__)
        self._token = self._config['sensor']['token']
        self._strip_formatting = self._config['sensor'].get('strip_formatting',
                                                            False)
        self._handlers = {
            'message': self._handle_message_ignore_errors,
        }

        self._user_info_cache = {}
        self._channel_info_cache = {}
        self._group_info_cache = {}

        self._last_message_timestamp = None

    def setup(self):
        self._client = SlackClient(self._token)
        data = self._client.rtm_connect()

        if not data:
            msg = 'Failed to connect to the Slack API. Invalid token?'
            raise Exception(msg)

        self._populate_cache(user_data=self._api_call('users.list'),
                             channel_data=self._api_call('channels.list'),
                             group_data=self._api_call('groups.list'),)

    def poll(self):
        result = self._client.rtm_read()

        if not result:
            return

        last_message_timestamp = self._handle_result(result=result)

        if last_message_timestamp:
            self._set_last_message_timestamp(
                last_message_timestamp=last_message_timestamp)

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _get_last_message_timestamp(self):
        """
        :rtype: ``int``
        """
        if not self._last_message_timestamp:
            name = self.DATASTORE_KEY_NAME
            value = self._sensor_service.get_value(name=name)
            self._last_message_timestamp = int(value) if value else 0

        return self._last_message_timestamp

    def _set_last_message_timestamp(self, last_message_timestamp):
        self._last_message_timestamp = last_message_timestamp
        name = self.DATASTORE_KEY_NAME
        value = str(last_message_timestamp)
        self._sensor_service.set_value(name=name, value=value)
        return last_message_timestamp

    def _populate_cache(self, user_data, channel_data, group_data):
        """
        Populate users, channels and group cache from info which is returned on
        rtm.start
        """

        for user in user_data.get('members', []):
            self._user_info_cache[user['id']] = user

        for channel in channel_data.get('channels', []):
            self._channel_info_cache[channel['id']] = channel

        for group in group_data.get('groups', []):
            self._group_info_cache[group['id']] = group

    def _handle_result(self, result):
        """
        Handle / process the result and return timestamp of the last message.
        """
        existing_last_message_timestamp = self._get_last_message_timestamp()
        new_last_message_timestamp = existing_last_message_timestamp

        for item in result:
            item_type = item['type']
            item_timestamp = int(float(item.get('ts', 0)))

            if (existing_last_message_timestamp and
                    item_timestamp <= existing_last_message_timestamp):
                # We have already seen this message, skip it
                continue

            if item_timestamp > new_last_message_timestamp:
                new_last_message_timestamp = item_timestamp

            handler_func = self._handlers.get(item_type, lambda data: data)
            handler_func(data=item)

        return new_last_message_timestamp

    def _handle_message(self, data):
        trigger = 'slack.message'
        event_type = data['type']

        if event_type not in EVENT_TYPE_WHITELIST or 'subtype' in data:
            # Skip unsupported event
            return

        # Note: We resolve user and channel information to provide more context
        user_info = self._get_user_info(user_id=data['user'])
        channel_info = None
        channel_id = data.get('channel', '')
        # Grabbing info based on the type of channel the message is in.
        if channel_id.startswith('C'):
            channel_info = self._get_channel_info(channel_id=channel_id)
        elif channel_id.startswith('G'):
            channel_info = self._get_group_info(group_id=channel_id)

        if not user_info or not channel_info:
            # Deleted user or channel
            return

        # Removes formatting from messages if enabled by the user in config
        if self._strip_formatting:
            text = re.sub("<http.*[|](.*)>", "\\1", data['text'])
        else:
            text = data['text']

        payload = {
            'user': {
                'id': user_info['id'],
                'name': user_info['name'],
                'first_name': user_info['profile'].get('first_name',
                                                       'Unknown'),
                'last_name': user_info['profile'].get('last_name',
                                                      'Unknown'),
                'real_name': user_info['profile'].get('real_name',
                                                      'Unknown'),
                'is_admin': user_info['is_admin'],
                'is_owner': user_info['is_owner']
            },
            'channel': {
                'id': channel_info['id'],
                'name': channel_info['name'],
                'topic': channel_info['topic']['value'],
                'is_group': channel_info.get('is_group', False),
            },
            'timestamp': int(float(data['ts'])),
            'timestamp_raw': data['ts'],
            'text': text
        }

        self._sensor_service.dispatch(trigger=trigger, payload=payload)

    def _handle_message_ignore_errors(self, data):
        try:
            self._handle_message(data)
        except Exception as exc:
            self._logger.info("Slack sensor encountered an error "
                              "handling message: %s" % exc)
            pass

    def _get_user_info(self, user_id):
        if user_id not in self._user_info_cache:
            result = self._api_call('users.info', user=user_id)

            if 'user' not in result:
                # User doesn't exist or other error
                return None

            result = result['user']
            self._user_info_cache[user_id] = result

        return self._user_info_cache[user_id]

    def _get_channel_info(self, channel_id):
        if channel_id not in self._channel_info_cache:
            result = self._api_call('channels.info', channel=channel_id)

            if 'channel' not in result:
                # Channel doesn't exist or other error
                return None

            result = result['channel']
            self._channel_info_cache[channel_id] = result

        return self._channel_info_cache[channel_id]

    def _get_group_info(self, group_id):
        if group_id not in self._group_info_cache:
            result = self._api_call('groups.info', channel=group_id)
            self._logger.warn('GROUP DATA: %s' % result)
            if 'group' not in result:
                # Group doesn't exist or other error
                return None

            result = result['group']
            self._group_info_cache[group_id] = result

        return self._group_info_cache[group_id]

    def _api_call(self, method, **kwargs):
        result = self._client.api_call(method, **kwargs)
        result = json.loads(result)
        return result
