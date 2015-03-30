import json

from lib.action import St2BaseAction

__all__ = [
    'St2KVPSetObjectAction'
]


class St2KVPSetObjectAction(St2BaseAction):
    def run(self, key, value):
        serialized_value = json.dumps(value)
        kvp = self._kvp(name=key, value=serialized_value)
        kvp.id = key
        update = self.client.keys.update(kvp)
        response = {
            'key': key,
            'value': value
        }
        return response
