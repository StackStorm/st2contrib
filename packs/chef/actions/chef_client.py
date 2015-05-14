#!/usr/bin/env python2.7

from lib.chef_runner import ChefRunner


class ChefClientRunner(ChefRunner):
    '''
    ChefRunner type implementation.
    Invokes chef-client binary with given arguments.
    '''

    chef_binary = 'chef-client'
    cmdline_options = [
        ('-r', '--rewrite_runlist', {})
    ]

    def __init__(self):
        self.cmdline_options += ChefRunner.cmdline_options


if __name__ == '__main__':
    runner = ChefClientRunner()
    runner.execute()
