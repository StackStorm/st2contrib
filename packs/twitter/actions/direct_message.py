from twitter import Twitter
from twitter import OAuth

from st2actions.runners.pythonrunner import Action

__all__ = [
    'DirectMessageAction'
]


class DirectMessageAction(Action):
    def run(self, screen_name, message):
        auth = OAuth(
            token=self.config['access_token'],
            token_secret=self.config['access_token_secret'],
            consumer_key=self.config['consumer_key'],
            consumer_secret=self.config['consumer_secret']
        )
        client = Twitter(auth=auth)
        client.direct_messages.new(user=screen_name, text=message)

        return True
