import copy
import salt.client

from st2actions.runners.pythonrunner import Action


class SaltClientAction(Action):
    def run(self, matches, module, args=None, kwargs=None):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        cli = salt.client.LocalClient()
        ret = cli.cmd(matches, module, arg=args, kwarg=kwargs)
        return ret
