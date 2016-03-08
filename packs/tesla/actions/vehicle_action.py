from lib.actions import BaseAction

__all__ = [
    'VehicleAction'
]


class VehicleAction(BaseAction):
    def run(self, vin, action, **kwargs):
        if vin is None:
            vehicle = self.connection.vehicles()[0]
        else:
            vehicle = self.connection.vehicle(vin)
        response = action = getattr(vehicle, action)(**kwargs)
        return self.formatter.formatter(response)
