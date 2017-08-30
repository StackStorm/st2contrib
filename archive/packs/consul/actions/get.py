from lib import action


class ConsulGetAction(action.ConsulBaseAction):
    def run(self, key, recurse, keys=False):
        list, value = self.consul.kv.get(key, recurse=recurse, keys=keys)
        return value
