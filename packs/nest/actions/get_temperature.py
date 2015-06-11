from lib import actions


class GetTemperatureAction(actions.BaseAction):
    def run(self, scale='c', structure=None, device=None):
        if structure and device:
            nest = self._get_device(structure, device)
        else:
            nest = self._get_default_device()

        return self._convert_temperature(nest.temperature, scale)
