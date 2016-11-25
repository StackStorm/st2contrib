from lib.sensu import SensuAction

__all__ = [
    'CheckListAction'
]


class CheckListAction(SensuAction):
    def run(self):
        return self.api.get_checks()
