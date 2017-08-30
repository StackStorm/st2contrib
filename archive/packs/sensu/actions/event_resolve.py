from lib.sensu import SensuAction

__all__ = [
    'EventResolveAction'
]


class EventResolveAction(SensuAction):
    def run(self, client, check):
        return self.api.post_event(client, check)
