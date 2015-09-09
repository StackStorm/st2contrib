from twitter import Twitter
from twitter import OAuth

from st2actions.runners.pythonrunner import Action

__all__ = [
    'FollowAction'
]


class FollowAction(Action):
    def run(self, screen_name):
        auth = OAuth(
            token=self.config['access_token'],
            token_secret=self.config['access_token_secret'],
            consumer_key=self.config['consumer_key'],
            consumer_secret=self.config['consumer_secret']
        )
        client = Twitter(auth=auth)
        client.friendships.create(screen_name=screen_name)

        return True
