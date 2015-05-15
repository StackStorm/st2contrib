from lib.action import St2BaseAction

__all__ = [
    'St2KVPGetAction'
]


class St2KVPGetAction(St2BaseAction):
    def run(self, key):
        _key = self.client.keys.get_by_name(key)

        if _key:
            return _key.value
        else:
            return False
