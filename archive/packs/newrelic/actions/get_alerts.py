import requests

from st2actions.runners.pythonrunner import Action


class GetAppHealthStatusAction(Action):
    """
    Get health status of new relic application(s).
    """
    def __init__(self, *args, **kwargs):
        super(GetAppHealthStatusAction, self).__init__(*args, **kwargs)
        self.url = 'https://api.newrelic.com/v2/applications.json'
        self.headers = {
            'User-Agent': 'StackStorm-New-Relic-Sensor/1.0.0 python-requests/2.7.0',
            'content-type': 'application/x-www-form-urlencoded',
        }
        self.headers['X-Api-Key'] = self.config['api_key']

    def run(self, app_name=None):
        params = None
        if app_name:
            params = {'filter[name]': app_name}

        resp = requests.get(self.url, headers=self.headers, params=params).json()

        app_status_map = {}
        for application in resp['applications']:
            app_status_map[application['name']] = application['health_status']

        return app_status_map
