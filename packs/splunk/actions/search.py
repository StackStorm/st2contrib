import splunklib.client as client

from st2actions.runners.pythonrunner import Action

__all__ = [
    'OneShotSearch'
]


class OneShotSearch(Action):

    def __init__(self, config):
        super(OneShotSearch, self).__init__(config)

        self.service = client.connect(
            host=self.config.get('host'),
            port=self.config.get('port'),
            username=self.config.get('username'),
            password=self.config.get('password'),
            scheme=self.config.get('scheme'))

    def run(self, search_query):
        kwargs_oneshot = {"output_mode": "json"}
        result = self.service.jobs.oneshot(search_query, **kwargs_oneshot)

        return result
