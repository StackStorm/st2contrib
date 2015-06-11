import bz2
import base64

from lib.action import St2BaseAction

__all__ = [
    'St2KVPSetAction'
]


class St2KVPSetAction(St2BaseAction):
    def run(self, key, value, ttl=None, compress=False):
        if compress:
            value = bz2.compress(value)
            value = base64.b64encode(value)

        kvp = self._kvp(name=key, value=value)
        kvp.id = key

        if ttl:
            kvp.ttl = ttl

        self.client.keys.update(kvp)
        response = {
            'key': key,
            'value': value,
            'ttl': ttl
        }
        return response
