from lib import action


class ConsulGetAction(action.ConsulBaseAction):
    def run(self, key, recurse, listing):
        list, value = self.consul.kv.get(key, recurse=recurse, keys=listing)
        return value
