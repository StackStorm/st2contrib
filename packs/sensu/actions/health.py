from lib.sensu import SensuAction

__all__ = [
    'HealthAction'
]


class HealthAction(SensuAction):
    def run(self, consumers, messages):
        return self.api.get_health(consumers, messages)
