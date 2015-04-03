from lib import actions

class GetHumidityAction(actions.BaseAction):
    def run(self, structure=0, device=0):
        nest = self._get_device(structure.device)
        return nest.humidity
