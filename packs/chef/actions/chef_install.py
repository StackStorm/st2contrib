#!/usr/bin/env python2.7

import sys

from lib import shellhelpers as shell


class ChefInstaller(object):
    #  from lib.omnibus import Omnibus

    '''
    Implements chef installation on the node.
    '''
    SUPPORTED_METHODS = ['omnibus']

    cmdline_options = [
        ('-m', '--method', {}),
        ('-p', '--pre_release', {'action': 'store_true'}),
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
        install_method = options['method']

        if not (install_method in self.SUPPORTED_METHODS):
            error = ("Chef pack doesn't support the given installation method: %s\n" %
                     (install_method))
            sys.stderr.write(error)
            sys.exit(1)

        del options['method']
        self.install(install_method, options)


if __name__ == '__main__':
    runner = ChefInstaller()
    runner.execute()
