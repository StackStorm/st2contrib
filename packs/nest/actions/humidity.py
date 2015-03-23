from lib import actions

class HumidityAction(actions.BaseAction):
    def run(self, structure, device, target=None):
        if target:
            target_humidity = target
        else:
            target_humidity = self._get_device(structure, device).humidity

        for structure in self._nest.structures:
            for device in structure.devices:
                device.target_humidity = target_humidity

        return target_humidity
