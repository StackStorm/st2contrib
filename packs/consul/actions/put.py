from lib import action


class ConsulPutAction(action.ConsulBaseAction):
    def run(self, key, value):
        return self.consul.kv.put(key, value)
