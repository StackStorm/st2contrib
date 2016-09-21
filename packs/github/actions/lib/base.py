from github import Github
import requests
from bs4 import BeautifulSoup
import json

from st2actions.runners.pythonrunner import Action

__all__ = [
    'BaseGithubAction'
]

# Default Github web URL (used by tasks which directly scrape data from HTML)
# pages
DEFAULT_WEB_URL = 'https://github.com'

# Default Github API url
DEFAULT_API_URL = 'https://api.github.com'


class BaseGithubAction(Action):
    def __init__(self, config):
        super(BaseGithubAction, self).__init__(config=config)
        token = self.config.get('token', None)
        self.token = token or None
        self.base_url = self.config.get('base_url', DEFAULT_API_URL)

        self._client = Github(self.token, base_url=self.base_url)
        self._session = requests.Session()

    def _web_session(self):
        '''Returns a requests session to scrape off the web'''
        login_url = DEFAULT_WEB_URL + '/login'
        session = requests.Session()
        request = session.get(login_url).text
        html = BeautifulSoup(request)
        token = html.find('input', {'name': 'authenticity_token'}).attrs['value']
        commit_value = html.find('input', {'name': 'commit'}).attrs['value']
        session_path = html.find('form', {'method': 'post'}).attrs['action']

        login_data = {
            'login': self.config['user'],
            'password': self.config['password'],
            'commit': commit_value,
            'authenticity_token': token
        }

        session_url = DEFAULT_WEB_URL + session_path
        session.post(session_url, data=login_data)
        return session

    def _get_analytics(self, category, repo):
        url = DEFAULT_WEB_URL + repo + '/graphs/' + category + '.json'
        s = self._web_session()
        response = s.get(url)
        return response.json()

    def _get_user_token(self, user):
        return self.action_service.get_value(
            name="token_{}".format(user))

    def _change_to_user_token(self, user):
        token = self.action_service.get_value(
            name="token_{}".format(user))

        self._client = Github(token, base_url=self.base_url)

        return True

    def _request(self, method, uri, payload, token):
        headers = {'Authorization': 'token {}'.format(token)}

        url = "{}{}".format(self.base_url,
                            uri)

        try:
            r = self._session.request(method,
                                      url,
                                      data=json.dumps(payload),
                                      headers=headers,
                                      verify=False)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            raise Exception(
                "ERROR: '{}'ing to '{}' - status code: {} payload: {}".format(
                    method, url, r.status_code, json.dumps(payload)))
        except requests.exceptions.ConnectionError, e:
            raise Exception("Could not connect to: {} : {}".format(url, e))
        else:
            if r.status_code == 204:
                return None
            else:
                return r.json()
