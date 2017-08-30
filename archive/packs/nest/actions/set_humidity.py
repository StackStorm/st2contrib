from lib import actions


class SetHumidityAction(actions.BaseAction):
    def run(self, target, structure=None, device=None):
        if structure and device:
            nest = self._get_device(structure, device)
            nest.target_humidity = target
        else:
            for structure in self._nest.structures:
                for device in structure.devices:
                    device.target_humidity = target

        return target
