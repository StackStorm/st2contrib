from lib.action import TravisCI


class ListHooksAction(TravisCI):
    def run(self):
        """
        Getting Hooks for user, returns id, name and state of hook
        """
        path = '/hooks'
        response = self._perform_request(path, method='GET', requires_auth=True)
        data = response.json()
        hooks = {}
        for hook in data['hooks']:
            hooks[hook['id']] = [hook['active'], hook['name']]
        return hooks
