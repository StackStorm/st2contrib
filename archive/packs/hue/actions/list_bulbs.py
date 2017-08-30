from lib import action


class ListBulbsAction(action.BaseAction):
    def run(self):
        bulbs = {}
        lights = self.hue.state['lights']

        for light_id, light in lights.iteritems():
            bulbs["l%s" % light_id] = light['name']

        return bulbs
