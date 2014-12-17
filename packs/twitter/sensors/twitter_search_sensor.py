from TwitterSearch import TwitterSearch
from TwitterSearch import TwitterSearchOrder


from st2reactor.sensor.base import PollingSensor


class TwitterSearchSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=None):
        super(TwitterSearchSensor, self).__init__(sensor_service=sensor_service,
                                                  config=config,
                                                  poll_interval=poll_interval)
        self._trigger_ref = 'twitter.matched_tweet'

    def setup(self):
        self._client = TwitterSearch(
            consumer_key=self._config['consumer_key'],
            consumer_secret=self._config['consumer_secret'],
            access_token=self._config['access_token'],
            access_token_secret=self._config['access_token_secret']
        )
        self._last_id = None

    def poll(self):
        tso = TwitterSearchOrder()
        tso.set_keywords(self._config['keywords'])

        language = self._config.get('language', None)
        if language:
            tso.set_language(language)

        tso.set_result_type('recent')
        tso.set_include_entities(False)

        if self._last_id:
            tso.set_since_id(self._last_id)

        tweets = list(self._client.search_tweets_iterable(tso))

        if tweets:
            self._last_id = tweets[0]['id']

        for tweet in tweets:
            self._dispatch_trigger_for_tweet(tweet=tweet)

    def cleanup(self):
        # TODO: Persist state (id) so we avoid duplicate events
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _dispatch_trigger_for_tweet(self, tweet):
        trigger = self._trigger_ref
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
            'text': tweet['text']
        }
        self._sensor_service.dispatch(trigger=trigger, payload=payload)
