from TwitterSearch import TwitterSearch
from TwitterSearch import TwitterSearchOrder
from TwitterSearch import TwitterSearchException

from st2reactor.sensor.base import PollingSensor

BASE_URL = 'https://twitter.com'


class TwitterSearchSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=None):
        super(TwitterSearchSensor, self).__init__(sensor_service=sensor_service,
                                                  config=config,
                                                  poll_interval=poll_interval)
        self._trigger_ref = 'twitter.matched_tweet'
        self._logger = self._sensor_service.get_logger(__name__)

        self._original_poll_interval = self.get_poll_interval()
        self._rate_limit_reached = False

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
        tso.set_keywords([self._config['query']])

        language = self._config.get('language', None)
        if language:
            tso.set_language(language)

        tso.set_result_type('recent')
        tso.set_count(self._config.get('count', 30))
        tso.set_include_entities(False)

        if self._last_id:
            tso.set_since_id(self._last_id)

        try:
            tweets = self._client.search_tweets(tso)
            tweets = tweets['content']['statuses']
        except TwitterSearchException as e:
            if e.code == 429:
                # Rate limit has been reached, increase poll interval
                self._rate_limit_reached = True

                current_poll_interval = self.get_poll_interval()
                new_poll_interval = (current_poll_interval * 2)

                message = ('Polling Twitter failed because rate limit has been reached %s. '
                           'Increaseing poll intervall to "%s" seconds' %
                           (str(e), new_poll_interval))
                self._logger.exception(message)

                self.set_poll_interval(poll_interval=new_poll_interval)
                return

            self._logger.exception('Polling Twitter failed: %s' % (str(e)))
            return
        except Exception as e:
            self._logger.exception('Polling Twitter failed: %s' % (str(e)))
            return

        if self._rate_limit_reached:
            # We are not rate limited anymore, restore original poll interval.
            self._rate_limit_reached = False
            self.set_poll_interval(poll_interval=self._original_poll_interval)

        tweets = list(reversed(tweets))

        if tweets:
            self._last_id = tweets[-1]['id']

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
