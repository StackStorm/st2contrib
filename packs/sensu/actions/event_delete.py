from lib.sensu import SensuAction

__all__ = [
    'EventDeleteAction'
]


class EventDeleteAction(SensuAction):
    def run(self, client, check):
        return self.api.delete_event(client, check)
