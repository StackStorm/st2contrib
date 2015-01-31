#!/usr/bin/env python2.7

import sys
import argparse
from lib import shellhelpers as shell

class ChefInstaller(object):
    from lib.omnibus import Omnibus

    '''
    Implements chef installation on the node.
    '''
    SUPPORTED_METHODS = [ 'omnibus' ]

    cmdline_options = [
        ('-o', '--omnibus', { 'action': 'store_true' }),
        ('-p', '--pre_release', { 'action': 'store_true' }),
        ('-v', '--version', {}),
        ('-d', '--download_path', {})
    ]


    def install(self, install_method, options):
        exit_code = 0
        installer = getattr(ChefInstaller, install_method.capitalize())(options)
        if not installer.chef_installed():
            exit_code = installer.install()
        else:
            sys.stdout.write("Chef is already installed, skipping installation...\n")
        sys.exit(exit_code)


    def execute(self):
        self.parser = shell.CmdlineParser(self.cmdline_options)
        options = self.parser.parse()
        install_method = [i for i in options.keys() if i in self.SUPPORTED_METHODS ]

        if len(install_method) > 1:
            sys.stderr.write("You can't use more than one installation method!\n")
            sys.stderr.write("Choose one of the following methods: %s\n" % ', '.join(self.SUPPORTED_METHODS))
            sys.exit(1)

        del(options[install_method[0]])
        self.install(install_method[0], options)


if __name__ == '__main__':
    runner = ChefInstaller()
    runner.execute()
