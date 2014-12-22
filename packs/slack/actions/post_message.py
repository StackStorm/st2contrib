import json
import httplib

import requests

from st2actions.runners.pythonrunner import Action

__all__ = [
    'PostMessageAction'
]


class PostMessageAction(Action):
    def run(self, message, username=None, icon_emoji=None):
        config = self.config['post_message_action']
        username = username if username else config['username']
        icon_emoji = icon_emoji if icon_emoji else config['icon_emoji']

        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        body = {
            'username': username,
            'icon_emoji': icon_emoji,
            'text': message
        }
        data = 'payload=%s' % (json.dumps(body))
        response = requests.post(url=config['webhook_url'],
                                 headers=headers, data=data)

        if response.status_code == httplib.OK:
            self.logger.info('Message successfully posted')
        else:
            self.logger.exception('Failed to post message: %s' % (response.text))

        return True
