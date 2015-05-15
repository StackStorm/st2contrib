import pygerduty

from st2actions.runners.pythonrunner import Action


class PagerDutyAction(Action):
    def __init__(self, config):
        super(PagerDutyAction, self).__init__(config)
        self.pager = self._init_client()
        self.trigger = []

    def _init_client(self):
        api_key = self.config['api_key']
        #  service_api = self.config['service_api']
        subdomain = self.config['subdomain']
        pager = pygerduty.PagerDuty(subdomain, api_token=api_key)
        return pager

    #  get all the acknowledged incidents
    def get_ack_incidents(self):
        ack_alarms = []
        for incident in self.pager.incidents.list(status="acknowledged"):
            ack_alarms.append(incident.incident_key)
        return ack_alarms

    #  get all the triggered incidents
    def get_triggered_incidents(self):
        trigger_alarms = []
        for incident in self.pager.incidents.list(status="triggered"):
            trigger_alarms.append(incident.incident_key)
        return trigger_alarms
