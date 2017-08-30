from lib.sensu import SensuAction

__all__ = [
    'CheckInfoAction'
]


class CheckInfoAction(SensuAction):
    def run(self, check):
        return self.api.get_check(check)
