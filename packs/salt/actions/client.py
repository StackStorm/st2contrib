import copy
import salt.client

from st2actions.runners.pythonrunner import Action


class SaltClientAction(Action):
    def run(self, matches, module, arguments=None):
        if arguments is None:
            arguments = []

        cli = salt.client.LocalClient()
        ret = cli.cmd(matches, module, arguments)
        return ret
