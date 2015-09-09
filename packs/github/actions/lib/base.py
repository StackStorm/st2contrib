from github import Github
import requests
from bs4 import BeautifulSoup

from st2actions.runners.pythonrunner import Action

__all__ = [
    'BaseGithubAction'
]

BASE_URL = 'https://github.com'


class BaseGithubAction(Action):
    def __init__(self, config):
        super(BaseGithubAction, self).__init__(config=config)
        token = self.config.get('token', None)
        token = token or None
        self._client = Github(token)

    def _web_session(self):
        '''Returns a requests session to scrape off the web'''
        login_url = BASE_URL + '/login'
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

        session_url = BASE_URL + session_path
        session.post(session_url, data=login_data)
        return session

    def _get_analytics(self, category, repo):
        url = 'https://github.com/' + repo + '/graphs/' + category
        s = self._web_session()
        response = s.get(url)
        return response.json()
