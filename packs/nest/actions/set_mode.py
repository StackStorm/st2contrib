from lib import actions


class SetModeAction(actions.BaseAction):
    def run(self, mode, structure=None, device=None):
        if structure and device:
            nest = self._get_device(structure, device)
            nest.mode = mode
        else:
            for structure in self._nest.structures:
                for device in structure.devices:
                    device.mode = mode

        return mode
