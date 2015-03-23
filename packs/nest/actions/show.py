from lib import actions

class ShowAction(actions.BaseAction):
    def run(self, structure, device):
        device = self._get_device(structure, device)
        data = device._shared.copy()
        data.update(device._device)

        return data
