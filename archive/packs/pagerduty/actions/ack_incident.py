from lib.action import PagerDutyAction


class AckIncident(PagerDutyAction):
    def run(self, event_keys):
        """
        Acknowledgment of a trigger, You can provide comma(,) separated keys for acknowledging more
        events at once.
        """

        for arg in event_keys:
            self.pager.acknowledge_incident(self.config['service_api'], arg)

        return event_keys
