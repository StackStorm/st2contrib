import copy
import salt.client

from st2actions.runners.pythonrunner import Action


class SaltClientAction(Action):
    def run(self, matches, module, args=None, kwargs=None):
        '''
        CLI Examples:

            st2 run salt.client matches='web*' module=test.ping
            st2 run salt.client module=pkg.install \
                    kwargs='{"pkgs":["git","httpd"]}'
        '''
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        cli = salt.client.LocalClient()
        ret = cli.cmd(matches, module, arg=args, kwarg=kwargs)
        return ret
