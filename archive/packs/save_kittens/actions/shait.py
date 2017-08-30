from __future__ import print_function

from Crypto.Hash import SHA

from st2actions.runners.pythonrunner import Action

__all__ = [
    'ShaIt'
]


class ShaIt(Action):
    def run(self, message, handle):
        sha_message = message + handle

        return SHA.new(sha_message).hexdigest()
