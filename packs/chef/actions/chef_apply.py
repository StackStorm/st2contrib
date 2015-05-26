#!/usr/bin/env python2.7

from lib.chef_runner import ChefRunner


class ChefApplyRunner(ChefRunner):
    '''
    ChefRunner type implementation.
    Invokes chef-client binary with given arguments.
    '''
    cmdline_options = [
        ('-j', '--attributes', {}),
        ('-l', '--log_level', {}),
        ('-e', '--execute', {}),
        ('-W', '--why_run', {'action': 'store_true'}),
        (None, '--minimal_ohai', {'action': 'store_true', 'translates': '--minimal-ohai'})
    ]

    def __init__(self):
        super(ChefApplyRunner, self).__init__()
        self.chef_binary = 'chef-apply'


if __name__ == '__main__':
    runner = ChefApplyRunner()
    runner.execute()
