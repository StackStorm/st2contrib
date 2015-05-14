from lib import actions


class GetModeAction(actions.BaseAction):
    def run(self, structure=None, device=None):
        if structure and device:
            nest = self._get_device(structure, device)
        else:
            nest = self._get_default_device()

        return nest.mode
