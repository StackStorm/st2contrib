# Licensed to the StackStorm, Inc ('StackStorm') under one or more

# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import six
import sys
import json

import eventlet
import requests
from flask import request, Flask
from six.moves import urllib_parse
from st2reactor.sensor.base import Sensor

eventlet.monkey_patch(
    os=True,
    select=True,
    socket=True,
    thread=False if '--use-debugger' in sys.argv else True,
    time=True)

PACK = 'newrelic'
WEB_APP_ALERT_TRIGGER_REF = '{}.{}'.format(PACK, 'WebAppAlertTrigger')
WEB_APP_NORMAL_TRIGGER_REF = '{}.{}'.format(PACK, 'WebAppNormalTrigger')
SERVER_ALERT_TRIGGER_REF = '{}.{}'.format(PACK, 'ServerAlertTrigger')
SERVER_NORMAL_TRIGGER_REF = '{}.{}'.format(PACK, 'ServerNormalTrigger')

NR_API_URL_KEY = 'api_url'
NR_API_KEY_KEY = 'api_key'

APP_HOST_KEY = 'host'
APP_PORT_KEY = 'port'
APP_URL_KEY = 'url'
NORMAL_REPORT_DELAY_KEY = 'normal_report_delay'


class NewRelicHookSensor(Sensor):
    """
    Sensor class that starts up a flask webapp that listens to alert hooks from NewRelic.
    It translates hooks into appropriate triggers using the following mapping -
       1. Web app incident and apdex problem opened -> WEB_APP_ALERT_TRIGGER
       2. Incident escalated to downtime (app)      -> WEB_APP_ALERT_TRIGGER
       3. Apdex problem closed (app)                -> WEB_APP_NORMAL_TRIGGER_REF
       4. Downtime problem closed (app)             -> WEB_APP_NORMAL_TRIGGER_REF
       5. Server incident and CPU problem opened    -> SERVER_ALERT_TRIGGER_REF
       6. Incident escalated after 5 minutes        -> SERVER_ALERT_TRIGGER_REF
       7. Server downtime ends                      -> SERVER_NORMAL_TRIGGER_REF
       8. CPU problem closed                        -> SERVER_NORMAL_TRIGGER_REF

    Note : Some hooks like cancel or disable of an inciden and open or close of alert policy
    are ignored.

    All return to normal events are always fired after a delay period.
    """

    def __init__(self, sensor_service, config=None):
        self._config = config
        self._sensor_service = sensor_service

        self._api_url = config.get(NR_API_URL_KEY, None)
        self._api_key = config.get(NR_API_KEY_KEY, None)

        self._host = self._get_sensor_config_param(self._config, APP_HOST_KEY)
        self._port = self._get_sensor_config_param(self._config, APP_PORT_KEY)
        self._url = self._get_sensor_config_param(self._config, APP_URL_KEY)
        self._normal_report_delay = self._get_sensor_config_param(self._config,
                                                                  NORMAL_REPORT_DELAY_KEY, 300)

        self._app = Flask(__name__)
        self._log = self._sensor_service.get_logger(__name__)
        self._headers = {'X-Api-Key': self._api_key}

    def setup(self):
        pass

    def run(self):
        """
        Validate required params and starts up the webapp that listen to hooks from NewRelic.
        """
        if not self._api_url:
            raise Exception('NewRelic API url not found.')
        if not self._api_key:
            raise Exception('NewRelic API key not found.')
        if not self._host or not self._port or not self._url:
            raise Exception('NewRelic webhook app config (host:%s, port:%s, url:%s)' %
                            (self._host, self._port, self._url))
        self._log.info('NewRelicHookSensor up. host %s, port %s, url %s', self._host, self._port,
                       self._url)

        @self._app.route(self._url, methods=['POST'])
        def handle_nrhook():

            # hooks are sent for alerts and deployments. Only care about alerts so ignoring
            # deployments. Body expected to be of the form -
            #
            # alert : {...}
            #      OR
            # deployment : {...}
            #
            # JSON inside form encoded data, seriously?
            data = request.form
            alert_body = data.get('alert', None)

            if not alert_body:
                self._log.info('Request doesn\'t contain "alert" attribute, ignoring...')
                return 'IGNORED'

            try:
                alert_body = json.loads(alert_body)
            except Exception:
                self._log.exception('Failed to parse request body: %s' % (alert_body))
                return 'IGNORED'

            if alert_body.get('severity', None) not in ['critical', 'downtime']:
                self._log.debug('Ignoring alert %s as it is not severe enough.', alert_body)
                return 'ACCEPTED'

            hook_headers = self._get_headers_as_dict(request.headers)
            hook_handler = self._get_hook_handler(alert_body, hook_headers)

            # all handling based off 'docs' found in this documentation -
            # https://docs.newrelic.com/docs/alerts/alert-policies/examples/webhook-examples

            try:
                if hook_handler:
                    hook_handler(alert_body, hook_headers)
            except Exception:
                self._log.exception('Failed to handle nr hook %s.', alert_body)

            return 'ACCEPTED'

        self._app.run(host=self._host, port=self._port)

    def _get_hook_handler(self, alert_body, hook_headers):
        if not alert_body:
            return None

        if 'servers' in alert_body:
            return self._server_hook_handler

        # For now everything else is web app hook. Hooks for key transaction, mobile app or plugin
        # alert all would be rolled up the application level.
        return self._app_hook_handler

    def _app_hook_handler(self, alert_body, hook_headers):
        if not alert_body['application_name']:
            self._log.info('No application found for alert %s. Will Ignore.', alert_body)
            return

        long_description = alert_body['long_description']

        if self._is_alert_opened(long_description) or \
           self._is_escalated_downtime(long_description):

            # handled opened and escalation to downtime immediately.
            payload = {
                'alert': alert_body,
                'header': hook_headers
            }
            self._dispatch_trigger(WEB_APP_ALERT_TRIGGER_REF, payload)

        elif (self._is_alert_closed(long_description) or
                self._is_downtime_recovered(long_description)):

            # handled closed and recovered after a delay.
            payload = {
                'alert': alert_body,
                'header': hook_headers
            }
            self._log.info('App alert closed. Delay.')
            eventlet.spawn_after(self._normal_report_delay, self._dispatch_application_normal,
                                 payload)

        elif (self._is_alert_canceled(long_description) or
                self._is_alert_acknowledged(long_description)):

            # ignore canceled or acknowledged
            self._log.info('Ignored alert : %s.', alert_body)

    def _dispatch_application_normal(self, payload, attempt_no=0):
        '''
        Dispatches WEB_APP_NORMAL_TRIGGER_REF if the application health_status is 'green'.
        '''
        # basic guard to avoid queuing up forever.
        if attempt_no == 10:
            self._log.warning('Abandoning WEB_APP_NORMAL_TRIGGER_REF dispatch. Payload %s', payload)
            return
        try:
            application = self._get_application(payload['alert']['application_name'])
            if application['health_status'] in ['green']:
                self._dispatch_trigger(WEB_APP_NORMAL_TRIGGER_REF, payload)
            else:
                self._log.info('Application %s has state %s. Rescheduling normal check.',
                               application['name'], application['health_status'])
                eventlet.spawn_after(self._normal_report_delay, self._dispatch_application_normal,
                                     payload, attempt_no + 1)
        except Exception:
            self._log.exception('Failed delay dispatch. Payload %s.', payload)

    def _server_hook_handler(self, alert_body, hook_headers):
        long_description = alert_body['long_description']
        if self._is_alert_opened(long_description) or \
           self._is_escalated_downtime(long_description):

            payload = {
                'alert': alert_body,
                'header': hook_headers
            }
            self._dispatch_trigger(SERVER_ALERT_TRIGGER_REF, payload)

        elif (self._is_alert_closed(long_description) or
                self._is_downtime_recovered(long_description)):

            payload = {
                'alert': alert_body,
                'header': hook_headers
            }
            self._log.info('App alert closed. Delay.')
            eventlet.spawn_after(self._normal_report_delay, self._dispatch_server_normal,
                                 payload)

        elif (self._is_alert_canceled(long_description) or
                self._is_alert_acknowledged(long_description)):
            self._log.info('Ignored alert : %s.', alert_body)

    def _dispatch_server_normal(self, payload, attempt_no=0):
        '''
        Dispatches SERVER_NORMAL_TRIGGER_REF if the all servers health_status is 'green'.
        '''
        # basic guard to avoid queuing up forever.
        if attempt_no == 10:
            self._log.warning('Abandoning SERVER_NORMAL_TRIGGER_REF dispatch. Payload %s', payload)
            return
        try:
            servers = self._get_servers(payload['alert']['servers'])
            # make sure all servers are ok.
            all_servers_ok = True
            for name, server in six.iteritems(servers):
                all_servers_ok &= server['health_status'] in ['green']
                if not all_servers_ok:
                    break

            if all_servers_ok:
                self._dispatch_trigger(SERVER_NORMAL_TRIGGER_REF, payload)
            else:
                for server in servers:
                    self._log.info('server %s has state %s. Rescheduling normal check.',
                                   server['name'], server['health_status'])
                eventlet.spawn_after(self._normal_report_delay, self._dispatch_server_normal,
                                     payload, attempt_no + 1)
        except:
            self._log.exception('Failed delay dispatch. Payload %s.', payload)

    def _dispatch_trigger(self, trigger, payload):
        self._sensor_service.dispatch(trigger, payload)
        self._log.info('Dispatched %s with payload %s.', trigger, payload)

    # alert test methods
    def _is_alert_opened(self, long_description):
        return long_description and long_description.startswith('Alert opened')

    def _is_alert_closed(self, long_description):
        return long_description and long_description.startswith('Alert ended')

    def _is_alert_canceled(self, long_description):
        return long_description and long_description.startswith('Alert canceled')

    def _is_alert_acknowledged(self, long_description):
        return long_description and long_description.startswith('Alert acknowledged')

    def _is_escalated_downtime(self, long_description):
        return long_description and long_description.startswith('Alert escalated to downtime')

    def _is_downtime_recovered(self, long_description):
        return long_description and long_description.startswith('Alert downtime recovered')

    # newrelic API methods
    def _get_application(self, app_name):
        params = None
        if app_name:
            params = {'filter[name]': app_name}
        url = urllib_parse.urljoin(self._api_url, 'applications.json')
        resp = requests.get(url, headers=self._headers, params=params).json()
        if 'applications' in resp:
            # pick 1st application
            return resp['applications'][0] if resp['applications'] else None
        return None

    def _get_servers(self, server_names):
        servers = {}
        # No batch query by name support so making API calls in a tight loop. Might be
        # ok to get all severs and filter manually but that gets complex for a large number
        # of server since the API pages data.
        for server_name in server_names:
            params = {'filter[name]': server_name}
            url = urllib_parse.urljoin(self._api_url, 'servers.json')
            resp = requests.get(url, headers=self._headers, params=params).json()
            servers[server_name] = resp['servers'][0] if resp['servers'] else None
        return servers

    @staticmethod
    def _get_sensor_config_param(config, param_name, default=None):
        sensor_config = NewRelicHookSensor._get_sensor_config(config)
        if sensor_config:
            return sensor_config.get(param_name, default)
        return default

    @staticmethod
    def _get_sensor_config(config):
        return config.get('sensor_config', None)

    @staticmethod
    def _get_headers_as_dict(headers):
        headers_dict = {}
        for k, v in headers:
            headers_dict[k] = v
        return headers_dict

    # ignore
    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass
