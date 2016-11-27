from lib.sensu import SensuAction

__all__ = [
    'ClientListAction'
]


class ClientListAction(SensuAction):
    def run(self, limit, offset):
        return self.api.get_clients(limit, offset)
