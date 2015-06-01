from lib.action import TravisCI
import requests
import yaml


class GetHooks(TravisCI):
    def run(self):
        """
        Getting Hooks for user, returns id,name and state of hook
        """
        _HEADERS = self.travis
        _HEADERS['Authorization'] = self.config["Authorization"]
        _HEADERS['Content-Type'] = self.config["Content-Type"]
        uri = self.config["uri"] + '/hooks'
        response = requests.get(uri, headers=_HEADERS)
        data = yaml.load(response.content)
        hooks = {}
        for hook in data['hooks']:
            hooks[hook['id']] = [hook['active'], hook['name']]
        return hooks
