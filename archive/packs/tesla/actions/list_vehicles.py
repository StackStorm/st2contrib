from lib.actions import BaseAction

__all__ = [
    'ListVehiclesAction'
]


class ListVehiclesAction(BaseAction):
    def run(self):
        return self.formatter.formatter(
            self.connection.vehicles())
