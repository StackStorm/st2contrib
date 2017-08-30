from rauth import OAuth1Session

from st2actions.runners.pythonrunner import Action

__all__ = [
    'BaseCubeSensorsAction',
]

BASE_URL = 'https://api.cubesensors.com/v1'


class BaseCubeSensorsAction(Action):
    def __init__(self, *args, **kwargs):
        super(BaseCubeSensorsAction, self).__init__(*args, **kwargs)
        self._session = OAuth1Session(consumer_key=self.config['consumer_key'],
                                      consumer_secret=self.config['consumer_secret'],
                                      access_token=self.config['access_token'],
                                      access_token_secret=self.config['access_token_secret'])

    def _perform_request(self, path, method='GET'):
        if not path.startswith('/'):
            path = '/' + path
        url = BASE_URL + path
        response = self._session.get(url)
        return response
