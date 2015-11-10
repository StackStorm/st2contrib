import requests
import urllib
import urlparse

from st2actions.runners.pythonrunner import Action

BASE_URL = 'https://slack.com/api/'


class SlackAction(Action):

    
    def run(self, **kwargs):
        if kwargs['token'] is None:
            kwargs['token'] = self.config['action_token']

        return self._get_request(kwargs)

    def _get_request(self, params):
        end_point = params['end_point']
        url = urlparse.urljoin(BASE_URL, end_point)
        del params['end_point']

        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        data = urllib.urlencode(params)
        self.logger.info(data)
        response = requests.get(url=url,
                                headers=headers, params=data)

        results = response.json()
        if not results['ok']:
            failure_reason = ('Failed to perform action %s: %s \
                              (status code: %s)' % (end_point, response.text,
                              response.status_code))
            self.logger.exception(failure_reason)
            raise Exception(failure_reason)

        return results
