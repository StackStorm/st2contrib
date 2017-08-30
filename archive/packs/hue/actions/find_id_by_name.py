from lib import action


class FindIDByNameAction(action.BaseAction):
    def run(self, name):
        light_id = None
        lights = self.hue.state['lights']

        for l_id, l in lights.iteritems():
            if l['name'] == name:
                light_id = l_id

        if light_id:
            return "l%s" % light_id
        else:
            error_msg = "Unknown Bulb"
            return error_msg
