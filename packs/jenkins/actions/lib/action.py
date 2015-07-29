from st2actions.runners.pythonrunner import Action
import jenkins


class JenkinsBaseAction(Action):

    def __init__(self, config):
        super(JenkinsBaseAction, self).__init__(config)
        self.jenkins = self._get_client()

    def _get_client(self):
        url = self.config['url']
        username = self.config['username']
        password = self.config['password']

        client = jenkins.Jenkins(url, username, password)
        return client
