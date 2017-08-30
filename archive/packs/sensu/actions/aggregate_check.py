from lib.sensu import SensuAction

__all__ = [
    'AggregateCheckAction'
]


class AggregateCheckAction(SensuAction):
    def run(self, check, age):
        return self.api.get_aggregate_check(check, age)
