from lib.sensu import SensuAction

__all__ = [
    'ClientInfoAction'
]


class ClientInfoAction(SensuAction):
    def run(self, client):
        return self.api.get_client_data(client)
