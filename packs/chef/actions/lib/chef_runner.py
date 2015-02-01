#!/usr/bin/env python2.7

import sys
from lib import shellhelpers as shell


class ChefRunner(object):
    '''
    ChefRunner type. Base for solo/client runners.
    '''

    chef_binary = None
    cmdline_options = [
        ('-j', '--attributes', {}),
        ('-E', '--environment', {}),
        ('-l', '--log_level', {}),
        ('-o', '--override_runlist', {}),
        ('-W', '--why_run', {'action': 'store_true'}),
    ]

    def __init__(self):
        pass

    def execute(self):
        parser = shell.CmdlineParser(self.cmdline_options)
        command = ([self._locate_binary(self.chef_binary)] +
                   parser.short_arglist())

        exit_code = shell.shell_out(command)
        sys.exit(exit_code)

    def _locate_binary(self, binary):
        return binary
