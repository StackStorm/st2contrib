from lib.action import TravisCI
import yaml


class ListHooksAction(TravisCI):
    def run(self):
        """
        Getting Hooks for user, returns id,name and state of hook
        """
        uri = self.config["uri"]+'/hooks'
        response = self._perform_request(uri, method="GET", requires_auth=True)
        data = yaml.load(response.content)
        hooks = {}
        for hook in data['hooks']:
            hooks[hook['id']] = [hook['active'], hook['name']]
        return hooks
