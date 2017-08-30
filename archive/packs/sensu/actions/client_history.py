from lib.sensu import SensuAction

__all__ = [
    'ClientHistoryAction'
]


class ClientHistoryAction(SensuAction):
    def run(self, client):
        return self.api.get_client_history(client)
