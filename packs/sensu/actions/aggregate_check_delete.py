from lib.sensu import SensuAction

__all__ = [
    'AggregateCheckDeleteAction'
]


class AggregateCheckDeleteAction(SensuAction):
    def run(self, check):
        return self.api.delete_aggregate(check)
