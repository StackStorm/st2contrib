from lib import action


class ToggleAction(action.BaseAction):
    def run(self, light_id, transition_time):
        light = self.hue.lights.get(light_id)
        light.toggle(transition_time)
