from lib.action import St2BaseAction

__all__ = [
    'St2KVPSetAction'
]

class St2KVPSetAction(St2BaseAction):
    def run(self, key, value):
        kvp = self._kvp(name=key, value=value)
        kvp.id = key
        update = self.client.keys.update(kvp)
        response = {
            'key': key,
            'value': value
        }
        return response

