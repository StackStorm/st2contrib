from lib import action


class SetStateAction(action.BaseAction):
    def run(self, light_id, state):
        light = self.hue.lights.get(light_id)
        light.set_state(state)
