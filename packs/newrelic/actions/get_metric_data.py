import requests

from st2actions.runners.pythonrunner import Action


class GetMetricDataAction(Action):
    """
    Get data for an application metric given time range.
    """
    def __init__(self, *args, **kwargs):
        super(GetMetricDataAction, Action).__init__(*args, **kwargs)
        self.base_url = 'https://api.newrelic.com/v2/applications/'
        # XXX: New Relic v2 APIs are supposed to be JSON but doc says XML.
        # https://docs.newrelic.com/docs/apm/apis/api-v2-examples/average-response-time-examples-api-v2
        self.metrics_url = '/metrics/data.xml'
        self.url = None
        self.headers = {
            'User-Agent': 'StackStorm New Relic Sensor/1.0.0 python-requests/2.7.0',
            'content-type': 'application/x-www-form-urlencoded',
        }
        self.headers['X-Api-Key'] = self.config['api_key']

    def run(self, app_id, metric_base_name,
            actual_metrics, time_from, time_to):
        body = self._get_body(metric_base_name, actual_metrics, time_from, time_to)
        self.url = self.base_url + app_id + self.metrics_url
        resp = requests.get(self.url, headers=self.headers, data=body).json()

        return resp

    def _get_body(self, metric_base_name, actual_metrics, time_from, time_to):
        params = 'names[]=' + metric_base_name
        params = params + '&' + '&'.join(['values[]=' + metric for metric in actual_metrics])
        params = params + '&' + 'from=' + time_from
        params = params + '&' + 'to=' + time_to
        params = params + '&' + 'summarize=' + 'true'
        return params
