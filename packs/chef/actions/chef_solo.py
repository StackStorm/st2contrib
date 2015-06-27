#!/usr/bin/env python2.7

from lib.chef_runner import ChefRunner


class ChefSoloRunner(ChefRunner):
    '''
    ChefRunner type implementation.
    Invokes chef-solo binary with given arguments.
    '''
    cmdline_options = [
        ('-r', '--recipe_url', {})
    ]

    def __init__(self):
        super(ChefSoloRunner, self).__init__()
        self.cmdline_options += ChefRunner.cmdline_options
        self.chef_binary = 'chef-solo'


if __name__ == '__main__':
    runner = ChefSoloRunner()
    runner.execute()
