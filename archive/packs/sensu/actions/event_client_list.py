from lib.sensu import SensuAction

__all__ = [
    'EventClientListAction'
]


class EventClientListAction(SensuAction):
    def run(self, client):
        return self.api.get_all_client_events(client)
