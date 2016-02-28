from lib import action


class ConsulGetAction(action.ConsulBaseAction):
    def run(self, key):
        list, value = self.consul.kv.get(key)
        return value
