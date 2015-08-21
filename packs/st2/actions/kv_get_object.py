import json

from lib.action import St2BaseAction

__all__ = [
    'St2KVPGetObjectAction'
]


class St2KVPGetObjectAction(St2BaseAction):
    def run(self, key):
        _key = self.client.keys.get_by_name(key)

        if _key:
            deserialized_value = json.loads(_key.value)
            return deserialized_value
        else:
            raise Exception("Key does not exist")
