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
        self.github_url = self.config.get('github_url', DEFAULT_API_URL)
        self.enterprise_url = self.config.get('enterprise_url', None)
        self.default_github_type = self.config.get('github_type', None)

        self._client = Github(self.token, base_url=self.github_url)
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

    def _is_enterprise(self, github_type):

        if github_type == "enterprise":
            return True
        elif github_type == "online":
            return False
        elif self.default_github_type == "enterprise":
            return True
        elif self.default_github_type == "online":
            return False
        else:
            raise ValueError("Default GitHub Invalid!")

    def _get_user_token(self, user, enterprise):
        """
        Return a users GitHub OAuth Token, if it fails replace '-'
        with '.' as '.' is not valid for GitHub names.
        """

        if enterprise:
            token_name = "token_enterprise_"
        else:
            token_name = "token_"

        token = self.action_service.get_value(token_name + user)

        # if a token is not returned, try using reversing changes made by
        # GitHub Enterpise during LDAP sync'ing.
        if token is None:
            token = self.action_service.get_value(
                token_name + user.replace("-", "."))

        return token

    def _change_to_user_token(self, user, enterprise=False):
        token = self._get_user_token(user, enterprise)

        if enterprise:
            self._client = Github(token, base_url=self.enterprise_url)
        else:
            self._client = Github(token, base_url=self.github_url)

        return True

    def _request(self, method, uri, payload, token, enterprise):
        headers = {'Authorization': 'token {}'.format(token)}

        if enterprise:
            url = "{}{}".format(self.enterprise_url, uri)
        else:
            url = "{}{}".format(self.github_url, uri)

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
