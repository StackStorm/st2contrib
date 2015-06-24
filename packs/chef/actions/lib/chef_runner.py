#!/usr/bin/env python2.7

import sys
from lib import shellhelpers as shell
from locate_binary import LocateBinary


class ChefRunner(LocateBinary, object):
    '''
    ChefRunner type. Base for solo/client runners.
    '''

    cmdline_options = [
        ('-j', '--attributes', {}),
        ('-E', '--environment', {}),
        ('-l', '--log_level', {}),
        ('-o', '--override_runlist', {}),
        ('-W', '--why_run', {'action': 'store_true'}),
    ]

    @property
    def chef_binary(self):
        if self._chef_binary is None:
            raise RuntimeError("self.chef_binary must be set")
        return self._chef_binary

    @chef_binary.setter
    def chef_binary(self, value):
        self._chef_binary = value

    def __init__(self):
        self._chef_binary = None

    def execute(self):
        parser = shell.CmdlineParser(self.cmdline_options)
        command = ([self.locate_binary(self.chef_binary)] +
                   parser.short_arglist())
        exit_code = shell.shell_out(command)
        sys.exit(exit_code)
