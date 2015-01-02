import json

import eventlet
from slackclient import SlackClient

from st2reactor.sensor.base import PollingSensor

eventlet.monkey_patch(
    os=True,
    select=True,
    socket=True,
    thread=True,
    time=True)


class SlackSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=None):
        super(SlackSensor, self).__init__(sensor_service=sensor_service,
                                          config=config,
                                          poll_interval=poll_interval)
        self._logger = self._sensor_service.get_logger(__name__)
        self._token = self._config['sensor']['token']
        self._handlers = {
            'message': self._handle_message
        }

        self._user_info_cache = {}
        self._channel_info_cache = {}

    def setup(self):
        self._client = SlackClient(self._token)
        data = self._client.rtm_connect()

        if not data:
            msg = 'Failed to connect to the Slack API. Invalid token?'
            raise Exception(msg)

        self._populate_cache(user_data=data['users'], channel_data=data['channels'])

    def poll(self):
        result = self._client.rtm_read()

        if result:
            self._handle_result(result=result)

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _populate_cache(self, user_data, channel_data):
        """
        Populate users and channels cache from info which is returned on
        rtm.start
        """
        for user in user_data:
            self._user_info_cache[user['id']] = user

        for channel in channel_data:
            self._channel_info_cache[channel['id']] = channel

    def _handle_result(self, result):
        for item in result:
            item_type = item['type']
            handler_func = self._handlers.get(item_type, lambda data: data)
            handler_func(data=item)

    def _handle_message(self, data):
        trigger = 'slack.message'

        # Note: We resolve user and channel information to provide more context
        user_info = self._get_user_info(user_id=data['user'])
        channel_info = self._get_channel_info(channel_id=data['channel'])

        payload = {
            'user': {
                'id': user_info['id'],
                'name': user_info['name'],
                'first_name': user_info['profile']['first_name'],
                'last_name': user_info['profile']['last_name'],
                'real_name': user_info['profile']['real_name'],
                'is_admin': user_info['is_admin'],
                'is_owner': user_info['is_owner']
            },
            'channel': {
                'id': channel_info['id'],
                'name': channel_info['name'],
                'topic': channel_info['topic']['value'],
            },
            'timestamp': int(float(data['ts'])),
            'text': data['text']
        }
        self._sensor_service.dispatch(trigger=trigger, payload=payload)

    def _get_user_info(self, user_id):
        if user_id not in self._user_info_cache:
            result = self._api_call('users.info', user=user_id)['user']
            self._user_info_cache[user_id] = result

        return self._user_info_cache[user_id]

    def _get_channel_info(self, channel_id):
        if channel_id not in self._channel_info_cache:
            result = self._api_call('channels.info', channel=channel_id)['channel']
            self._channel_info_cache[channel_id] = result

        return self._channel_info_cache[channel_id]

    def _api_call(self, method, **kwargs):
        result = self._client.api_call(method, **kwargs)
        result = json.loads(result)
        return result
