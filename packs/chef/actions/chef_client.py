#!/usr/bin/env python2.7

from lib.chef_runner import ChefRunner


class ChefClientRunner(ChefRunner):
    '''
    ChefRunner type implementation.
    Invokes chef-client binary with given arguments.
    '''
    cmdline_options = [
        ('-r', '--rewrite_runlist', {})
    ]

    def __init__(self):
        super(ChefClientRunner, self).__init__()
        self.cmdline_options += ChefRunner.cmdline_options
        self.chef_binary = 'chef-client'


if __name__ == '__main__':
    runner = ChefClientRunner()
    runner.execute()
