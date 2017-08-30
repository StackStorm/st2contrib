from lib import action


class OnAction(action.BaseAction):
    def run(self, light_id, transition_time):
        light = self.hue.lights.get(light_id)
        light.on(transition_time)
