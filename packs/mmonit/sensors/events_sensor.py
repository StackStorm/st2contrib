import requests
from st2reactor.sensor.base import PollingSensor


class MmonitEventsSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=5):
        super(MmonitEventsSensor, self).__init__(sensor_service=sensor_service,
                                                 config=config,
                                                 poll_interval=poll_interval)

    def setup(self):
        self.url = self._config["shared_sensors_config"]["host"].strip("/")
        self.user = self._config["shared_sensors_config"]["user"]
        self.password = self._config["shared_sensors_config"]["password"]
        self.session = requests.session()
        self._login()

    def _login(self):
        self.session.get(self.url)
        data = {"z_csrf_protection": "off",
                "z_username": self.user,
                "z_password": self.password}
        login = self.session.get("{}/z_security_check".format(self.url), data=data)
        if login.status_code != 200:
            raise Exception("Could not login to mmonit {}".format(login.reason))

    def poll(self):
        # always check for status_code on a secured page on each poll in case we get logged out
        test_login = self.session.get("{}/session/get".format(self.url))
        if test_login.status_code != 200:
            self._login()

        events_list = self.session.get("{}/reports/events/list".format(self.url)).json()
        events = self._clear_list(events_list)
        for event in events:
            payload = {"host": event['hostname'], "id": event['id'],
                       "event": event['event'], "servicename": event["servicename"],
                       "full_data": event}
            self._sensor_service.dispatch(trigger="mmonit.new_event", payload=payload)
            self._sensor_service.set_value('monit.last_event', event["id"])

    def cleanup(self):
        self.session.get("{}/login/logout.csp".format(self.url))
        self.session.close()

    def _clear_list(self, events):
        last_event = self._sensor_service.get_value('monit.last_event')
        for index, item in enumerate(events['records']):
            if item['id'] > last_event:
                events['records'].pop(index)
        return events['records']

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass
