from lib import action


class ColorTempMiredAction(action.BaseAction):
    def run(self, light_id, temperature, transition_time):
        light = self.hue.lights.get(light_id)
        light.ct(temperature, transition_time)
