from lib.action import PagerDutyAction


class OpenIncident(PagerDutyAction):
    def run(self):
        """List all Open incidents """
        open_incident = {}
        open_incident_list = []
        for incident in self.pager.incidents.list(status="triggered,acknowledged"):
            open_incident = {'key': incident.incident_key, 'status': incident.status,
                             'desc': incident.trigger_summary_data.description}
            open_incident_list.append(open_incident)
        return open_incident_list
