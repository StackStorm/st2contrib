from lib import action


class BrightnessAction(action.BaseAction):
    def run(self, light_id, brightness, transition_time):
        light = self.hue.lights.get(light_id)
        light.bri(brightness, transition_time)
