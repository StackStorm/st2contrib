from lib.action import PagerDutyAction


class ResolveIncident(PagerDutyAction):
    def run(self, event_keys):
        """
        Resolve an incident, You can provide comma(,) separated keys for resolving more events at
        once.
        """
        for arg in event_keys:
            self.pager.resolve_incident(self.config['service_api'], arg)

        return event_keys
