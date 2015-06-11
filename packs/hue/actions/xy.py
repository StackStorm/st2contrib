from lib import action


class XYAction(action.BaseAction):
    def run(self, x, y, light_id, transition_time):
        light = self.hue.lights.get(light_id)
        light.xy(x, y, transition_time)
