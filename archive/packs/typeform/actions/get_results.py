import httplib
import requests
import urllib
import urlparse

from st2actions.runners.pythonrunner import Action

__all__ = [
    'TypeformAction'
]

BASE_URL = 'https://api.typeform.com/v0/form/'


class TypeformAction(Action):

    def run(self, form_id, api_key, completed=True):
        api_key = api_key if api_key else self.config['api_key']
        completed = str(completed).lower()
        url = urlparse.urljoin(BASE_URL, form_id)

        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        params = {"key": api_key,
                  "completed": completed
                  }

        data = urllib.urlencode(params)
        response = requests.get(url=url,
                                headers=headers, params=data)

        if response.status_code != httplib.OK:
            failure_reason = ('Failed to retrieve registrations: %s \
                (status code: %s)' %
                              (response.text, response.status_code))
            self.logger.exception(failure_reason)
            raise Exception(failure_reason)

        return response.json()
