#!/usr/bin/env python2.7

import sys
import argparse
from lib.shell_out import shell_out

class ChefRunner(object):
    '''
    ChefRunner type. Base for solo/client runners.
    '''

    chef_binary = None
    cmdline_options = [
        ('-j', 'attributes', {}),
        ('-E', 'environment', {}),
        ('-l', 'log_level', {}),
        ('-o', 'override_runlist', {}),
        ('-W', 'why_run', {'action': 'store_true'}),
    ]

    def __init__(self):
        pass

    def execute(self):
        command = [ self._locate_binary(self.chef_binary) ] + self._cmdline_args()
        exit_code = shell_out(command)
        sys.exit(exit_code)

    # Creates chef command line argument list.
    def _cmdline_args(self):
        cmd = []
        parser = argparse.ArgumentParser()
        for k, name, kwargs in self.cmdline_options:
            parser.add_argument(k, "--%s" % name , **kwargs)

        args = vars(parser.parse_args())
        for k, n, _ in self.cmdline_options:
            if not args[n]: continue
            # We handle switch if argument value is True
            cmd += [k] if args[n] == True else [k, args[n]]

        return cmd

    def _locate_binary(self, binary):
        return binary
