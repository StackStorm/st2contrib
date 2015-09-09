from lib import actions


class ShowAction(actions.BaseAction):
    def run(self, structure=None, device=None):
        if structure and device:
            device = self._get_device(structure, device)
        else:
            device = self._get_default_device()

        data = device._shared.copy()
        data.update(device._device)

        return data
