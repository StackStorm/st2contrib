from lib import actions

class ModeAction(actions.BaseAction):
    def run(self, mode, structure, device):
        if mode:
            target_mode = mode
            for structure in self._nest.structures:
                for device in structure.devices:
                    device.mode = target_mode
        else:
            target_mode = self._get_device(structure, device).mode

        return target_mode
