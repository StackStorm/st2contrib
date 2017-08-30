from lib.sensu import SensuAction

__all__ = [
    'EventInfoAction'
]


class EventInfoAction(SensuAction):
    def run(self, client, check):
        return self.api.get_event(client, check)
