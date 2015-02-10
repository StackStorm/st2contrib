from lib.base import BaseGPGAction

__all__ = [
    'ListKeysAction'
]


class ListKeysAction(BaseGPGAction):
    def run(self):
        keys = self._gpg.list_keys()
        return keys
