from lib import action


class ConsulDeleteAction(action.ConsulBaseAction):
    def run(self, key, recurse):
        return self.consul.kv.delete(key, recurse=recurse)
