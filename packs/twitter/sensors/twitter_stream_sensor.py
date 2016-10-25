from twython import TwythonStreamer

from st2reactor.sensor.base import Sensor

__all__ = [
    'TwitterStreamSensor'
]

BASE_URL = 'https://twitter.com'


class TwitterStreamHandler(TwythonStreamer):
    def __init__(self, consumer_key, consumer_secret, token, token_secret, callback):
        super(TwitterStreamHandler, self).__init__(
            consumer_key,
            consumer_secret,
            token,
            token_secret
        )

        self._callback = callback

    def on_success(self, data):
        if 'text' in data:
            self._callback(tweet=data)

    def on_error(self, status_code, data):
        print status_code


class TwitterStreamSensor(Sensor):
    def __init__(self, sensor_service, config=None):
        super(TwitterStreamSensor, self).__init__(
            sensor_service=sensor_service,
            config=config
        )
        self._trigger_ref = 'twitter.stream_matched_tweet'
        self._logger = self._sensor_service.get_logger(__name__)

    def setup(self):
        pass

    def run(self):
        twitter = TwitterStreamHandler(
            self._config['consumer_key'],
            self._config['consumer_secret'],
            self._config['access_token'],
            self._config['access_token_secret'],
            self._dispatch_trigger_for_tweet
        )
        twitter.user()

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _dispatch_trigger_for_tweet(self, tweet):
        trigger = self._trigger_ref

        url = '%s/%s/status/%s' % (BASE_URL, tweet['user']['screen_name'], tweet['id'])
        payload = {
            'id': tweet['id'],
            'created_at': tweet['created_at'],
            'lang': tweet['lang'],
            'place': tweet['place'],
            'retweet_count': tweet['retweet_count'],
            'favorite_count': tweet['favorite_count'],
            'user': {
                'screen_name': tweet['user']['screen_name'],
                'name': tweet['user']['name'],
                'location': tweet['user']['location'],
                'description': tweet['user']['description'],
            },
            'text': tweet['text'],
            'url': url
        }
        self._sensor_service.dispatch(trigger=trigger, payload=payload)
