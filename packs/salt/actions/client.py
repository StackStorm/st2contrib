import salt.client

from st2actions.runners.pythonrunner import Action


class SaltClientAction(Action):
    def run(self, matches, module, args=[], kwargs={}):
        '''
        CLI Examples:

            st2 run salt.client matches='web*' module=test.ping
            st2 run salt.client module=pkg.install \
                    kwargs='{"pkgs":["git","httpd"]}'
        '''
        cli = salt.client.LocalClient()
        ret = cli.cmd(matches, module, arg=args, kwarg=kwargs)
        return ret
