from lib import actions

class GetTemperatureAction(actions.BaseAction):
    def run(self, scale='c', structure=0, device=0):
        nest = self._get_device(structure, device)
        return self._convert_temperature(nest.temperature, scale)

