from lib.actions import BaseAction

__all__ = [
    'GetVehicleAction'
]


class GetVehicleAction(BaseAction):
    def run(self, vin):
        return self.formatter.formatter(
            self.connection.vehicle(vin))
