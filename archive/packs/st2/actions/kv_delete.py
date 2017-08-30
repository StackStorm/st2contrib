from lib.action import St2BaseAction

__all__ = [
    'St2KVPDeleteAction'
]


class St2KVPDeleteAction(St2BaseAction):
    def run(self, key):
        _key = self.client.keys.get_by_name(key)

        if _key:
            _key.id = key
            return self.client.keys.delete(_key)
        else:
            return False
