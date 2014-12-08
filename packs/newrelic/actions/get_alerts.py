import requests

from st2actions.runners.pythonrunner import Action


class GetAppHealthStatusAction(Action):
    """
    Get health status of new relic application(s).
    """
    def __init__(self, *args, **kwargs):
        super(GetAppHealthStatusAction, Action).__init__(*args, **kwargs)
        self.url = 'https://api.newrelic.com/v2/applications.json'
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }
        self.headers['X-Api-Key'] = self.config['api_key']

    def run(self, app_name=None):
        # XXX: New Relic APIs allow you to filter just based on app_name
        # but it doesn't work.
        body = None
        if app_name:
            app_name.replace(' ', '+')
            body = 'filter[name]=' + app_name

        resp = requests.get(self.url, headers=self.headers, data=body).json()

        app_status_map = {}
        for application in resp['applications']:
            app_status_map[application['name']] = application['health_status']

        return app_status_map
