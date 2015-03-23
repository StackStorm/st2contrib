from lib import actions

class FanAction(actions.BaseAction):
    def run(self, state, structure, device):
        if state == 'on':
            target_state = True
        else:
            target_state = False

        for structure in self._nest.structures:
            for device in structure.devices:
                device.fan = target_state

        return state
