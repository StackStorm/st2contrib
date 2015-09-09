import requests

from st2actions.runners.pythonrunner import Action


class KillWorkflow(Action):
    EXEC_BASE_URL = None

    def run(self, execution_id, kill_msg='Killed'):
        payload = {'state': 'ERROR', 'state_info': kill_msg}
        resp = requests.put(self._get_exec_url(execution_id), data=payload)
        return resp.json()

    def _get_exec_url(self, execution_id):
        if not KillWorkflow.EXEC_BASE_URL:
            host = self.config['host']
            api_version = self.config['api_version']
            url = host + api_version + '/executions/'
            KillWorkflow.EXEC_BASE_URL = url

        return KillWorkflow.EXEC_BASE_URL + execution_id
