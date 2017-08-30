"""WebPageTest actions."""

import random
import requests
from st2actions.runners.pythonrunner import Action

__all__ = ['WebPageTestAction']


class WebPageTestAction(Action):
    def __init__(self, config):
        super(WebPageTestAction, self).__init__(config=config)
        self.wpt_url = config.get('wpt_url', 'http://webpagetest.org')
        self.key = config.get('key', None)

    def list_locations(self):
        """Return available locations."""
        params = {'f': 'json'}
        if self.key:
            params['k'] = self.key
        request = requests.get("{0}/getLocations.php".format(self.wpt_url),
                               params=params)
        locations = request.json()['data']
        return sorted(locations.keys())

    def request_test(self, domain, location):
        """
        Execute a test for the given domain at a specific location.
        Optional key is required for Google's public instance.
        """
        params = {'f': 'json', 'url': domain, 'location': location}
        if self.key:
            params['k'] = self.key

        request = requests.get("{0}/runtest.php".format(self.wpt_url),
                               params=params)
        return request.json()

    def get_test_results(self, test_id):
        """
        Retrieve test results.
        Optional key is required for Google's public instance.
        """
        params = {'test': test_id}
        if self.key:
            params['k'] = self.key

        request = requests.get("{0}/jsonResult.php".format(self.wpt_url),
                               params=params)
        return request.json()

    def test_random_location(self, domain):
        """
        Execute a test for the given domain at a random location.
        Optional key is required for Google's public instance.
        """
        locations = self.list_locations()
        test = self.request_test(domain, random.choice(locations))
        try:
            return test['data']['userUrl']
        except KeyError:
            return "Error: {0}".format(test)
