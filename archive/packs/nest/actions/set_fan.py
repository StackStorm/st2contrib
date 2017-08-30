from lib import actions


class SetFanAction(actions.BaseAction):
    def run(self, state, structure=None, device=None):
        target_state = True if state == 'on' else False

        if structure and device:
            nest = self._get_device(structure, device)
            nest.fan = target_state
        else:
            for structure in self._nest.structures:
                for device in structure.devices:
                    device.fan = target_state

        return state
