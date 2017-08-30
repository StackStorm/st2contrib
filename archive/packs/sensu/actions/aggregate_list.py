from lib.sensu import SensuAction

__all__ = [
    'AggregateListAction'
]


class AggregateListAction(SensuAction):
    def run(self):
        return self.api.get_aggregates()
