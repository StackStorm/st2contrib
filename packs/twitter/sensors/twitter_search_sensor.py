from TwitterSearch import TwitterSearch
from TwitterSearch import TwitterSearchOrder

from st2reactor.sensor.base import PollingSensor

__all__ = [
    'TwitterSearchSensor'
]

BASE_URL = 'https://twitter.com'


class TwitterSearchSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=None):
        super(TwitterSearchSensor, self).__init__(sensor_service=sensor_service,
                                                  config=config,
                                                  poll_interval=poll_interval)
        self._trigger_ref = 'twitter.matched_tweet'
        self._logger = self._sensor_service.get_logger(__name__)

    def setup(self):
        self._client = TwitterSearch(
            consumer_key=self._config['consumer_key'],
            consumer_secret=self._config['consumer_secret'],
            access_token=self._config['access_token'],
            access_token_secret=self._config['access_token_secret']
        )
        self._last_id = None

        if type(self._config['query']) is not list:
            self._logger.exception('Twitter sensor failed. "query" config \
                                    value is not a list')
            raise ValueError('[TwitterSearchSensor]: "query" is not a list')

    def poll(self):
        tso = TwitterSearchOrder()
        tso.set_keywords(self._config['query'])

        language = self._config.get('language', None)
        if language:
            tso.set_language(language)

        tso.set_result_type('recent')
        tso.set_count(self._config.get('count', 30))
        tso.set_include_entities(False)

        last_id = self._get_last_id()

        if last_id:
            tso.set_since_id(int(last_id))

        try:
            tweets = self._client.search_tweets(tso)
            tweets = tweets['content']['statuses']
        except Exception as e:
            self._logger.exception('Polling Twitter failed: %s' % (str(e)))
            return

        tweets = list(reversed(tweets))

        if tweets:
            self._set_last_id(last_id=tweets[-1]['id'])

        for tweet in tweets:
            self._dispatch_trigger_for_tweet(tweet=tweet)

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _get_last_id(self):
        if not self._last_id and hasattr(self._sensor_service, 'get_value'):
            self._last_id = self._sensor_service.get_value(name='last_id')

        return self._last_id

    def _set_last_id(self, last_id):
        self._last_id = last_id

        if hasattr(self._sensor_service, 'set_value'):
            self._sensor_service.set_value(name='last_id', value=last_id)

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
