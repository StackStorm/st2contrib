from lib import action


class RGBAction(action.BaseAction):
    def run(self, light_id, red, green, blue, transition_time):
        light = self.hue.lights.get(light_id)
        light.rgb(red, green, blue, transition_time)
