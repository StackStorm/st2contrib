from lib.sensu import SensuAction

__all__ = [
    'EventListAction'
]


class EventListAction(SensuAction):
    def run(self):
        return self.api.get_events()
