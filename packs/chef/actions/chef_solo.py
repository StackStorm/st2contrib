#!/usr/bin/env python2.7

from lib.chef_runner import ChefRunner

class ChefSoloRunner(ChefRunner):
    '''
    ChefRunner type implementation.
    Invokes chef-solo binary with given arguments.
    '''

    chef_binary = 'chef-solo'
    cmdline_options = [
        ('-r', 'recipe_url', {})
    ]

    def __init__(self):
        self.cmdline_options += ChefRunner.cmdline_options


if __name__ == '__main__':
    runner = ChefSoloRunner()
    runner.execute()
