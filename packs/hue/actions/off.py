from lib import action


class OffAction(action.BaseAction):
    def run(self, light_id, transition_time):
        light = self.hue.lights.get(light_id)
        light.off(transition_time)
