import eventlet
import requests
from datetime import datetime

from st2reactor.sensor.base import PollingSensor

__all_ = [
    'DripstatAlertSensor'
]

BASE_URL = 'https://api.dripstat.com/api/v1'

eventlet.monkey_patch(
    os=True,
    select=True,
    socket=True,
    thread=True,
    time=True)


class DripstatAlertSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=30):
        super(DripstatAlertSensor, self).__init__(sensor_service=sensor_service,
                                                  config=config,
                                                  poll_interval=poll_interval)
        self._trigger_ref = 'dripstat.alert'
        self._log = self._sensor_service.get_logger(__name__)

    def setup(self):
        self._api_key = self._config['api_key']
        self._applications = self._api_request(endpoint='/apps')

    def poll(self):
        for application in self._applications:
            params = {'appId': application['id']}
            alerts = self._api_request(endpoint='/activeAlerts', params=params)
            for alert in alerts:
                last_alert_timestamp = self._get_last_alert_timestamp(application['name'])
                epoch = int(alert['startedAt']) / 1000
                if epoch > last_alert_timestamp:
                    self._set_last_alert_timestamp(application['name'], epoch)
                    self._dispatch_trigger_for_alert(application=application['name'], alert=alert,
                                                     epoch=epoch)

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _api_request(self, endpoint, params={}):
        url = BASE_URL + endpoint
        default_params = {'clientId': self._api_key}
        params.update(default_params)
        response = requests.get(url, params=params)
        return response.json()

    def _dispatch_trigger_for_alert(self, application, alert, epoch):
        trigger = self._trigger_ref
        payload = {
            'app_name': application,
            'alert_type': alert['name'],
            'started_at': epoch,
            'started_at_iso8601': datetime.fromtimestamp(epoch).isoformat(),
            'jvm_host': alert['jvmHost']
        }
        self._sensor_service.dispatch(trigger=trigger, payload=payload)

    def _get_last_alert_timestamp(self, app):
        last_alert_timestamp = self._sensor_service.get_value("%s.last_alert_timestamp" % app)

        if last_alert_timestamp:
            return int(last_alert_timestamp)
        else:
            return 0

    def _set_last_alert_timestamp(self, app, timestamp):
        self._sensor_service.set_value(name='%s.last_alert_timestamp' % app, value=str(timestamp))
