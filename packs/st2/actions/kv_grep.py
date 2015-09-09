from lib.action import St2BaseAction

__all__ = [
    'St2KVPGrepAction'
]


class St2KVPGrepAction(St2BaseAction):
    def run(self, query):
        _keys = self.client.keys.get_all()
        results = {}
        for key in _keys:
            if query in key.name:
                results[key.name] = key.value

        return results
