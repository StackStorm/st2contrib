from lib.sensu import SensuAction

__all__ = [
    'InfoAction'
]


class InfoAction(SensuAction):
    def run(self):
        return self.api.get_info()
