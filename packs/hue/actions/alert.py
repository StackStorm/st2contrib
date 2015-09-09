from lib import action


class ToggleAction(action.BaseAction):
    def run(self, light_id, long_alert=False):
        light = self.hue.lights.get(light_id)
        if long_alert:
            light.alert('lselect')
        else:
            light.alert()
