from lib.sensu import SensuAction

__all__ = [
    'ClientDeleteAction'
]


class ClientDeleteAction(SensuAction):
    def run(self, client):
        return self.api.delete_client(client)
