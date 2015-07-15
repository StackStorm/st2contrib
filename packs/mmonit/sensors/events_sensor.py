import requests
from st2reactor.sensor.base import PollingSensor


class MmonitEventsSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=5):
        super(MmonitEventsSensor, self).__init__(sensor_service=sensor_service,
                                                 config=config,
                                                 poll_interval=poll_interval)

    def setup(self):
        self._logger = self._sensor_service.get_logger(name=self.__class__.__name__)
        self.url = self._config['shared_sensors_config']['host'].strip('/')
        self.user = self._config['shared_sensors_config']['username']
        self.password = self._config['shared_sensors_config']['password']
        self.active = self._config['shared_sensors_config']['active']
        self.event_types = self._config['shared_sensors_config']['event_types'].split(',')
        self.session = requests.session()
        self._login()

    def _login(self):
        self.session.get(self.url)
        data = {'z_csrf_protection': 'off',
                'z_username': self.user,
                'z_password': self.password}
        login = self.session.post('{}/z_security_check'.format(self.url), data=data)
        if login.status_code != 200:
            raise Exception('Could not login to mmonit {}'.format(login.reason))

    def poll(self):
        # always check for status_code on a secured page on each poll in case we get logged out
        test_login = self.session.get('{}/session/get'.format(self.url))
        if test_login.status_code != 200:
            self._login()

        events_list = self.session.get('{}/reports/events/list'.format(self.url),
                                       params={'active': self.active}).json()
        events = self._clear_list(events_list)
        self._clear_datastore(events_list)
        for event in events:
            payload = {'host': event['hostname'], 'id': event['id'],
                       'event': event['event'], 'servicename': event['servicename'],
                       'full_data': event}
            self._sensor_service.dispatch(trigger='mmonit.new_event', payload=payload)
            self._sensor_service.set_value(str(event['id']), event['id'])

    def cleanup(self):
        self.session.get('{}/login/logout.csp'.format(self.url))
        self.session.close()

    def _clear_datastore(self, events):
        """As we store the triggered events in the datastore,
        this checks if the actual standing alerts
        from monit are in the datastore, and if they are not
        then we remove them so they can be triggered again
        in case the alert arises again"""
        active_events = [str(item['id']) for item in events['records']]
        for k in self._sensor_service.list_values():
            if str(k.value) not in active_events:
                self._logger.debug('Event {} is no longer active, '
                                   'deleting from the datastore'.format(k.value))
                self._sensor_service.delete_value(k.value)

    def _clear_list(self, events):
        """Removes already triggered events from the events list.
        This makes long standing alerts
        that had already been triggered, not get triggered again."""
        triggered_events = [str(kvp.value) for kvp in self._sensor_service.list_values()]
        new_list = []
        for item in events['records']:
            if str(item['id']) in triggered_events:
                self._logger.debug('Event {} was already triggered, '
                                   'not triggering it anymore.'.format(item['id']))
            elif str(item['eventtype']) not in self.event_types:
                self._logger.debug('Event {} was filtered by the configuration.'.format(item['id']))
            else:
                self._logger.debug('Event {} looks new. Triggering!'.format(item['id']))
                new_list.append(item)
        return new_list

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass
