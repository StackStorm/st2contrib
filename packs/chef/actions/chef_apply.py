#!/usr/bin/env python2.7

import sys
from lib import shellhelpers as shell
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
        (None, '--minimal_ohai', {'action': 'store_true'}),
        (None, '--recipe_file', {})
    ]

    def __init__(self):
        super(ChefApplyRunner, self).__init__()
        self.chef_binary = 'chef-apply'

    def execute(self):
        parser = shell.CmdlineParser(self.cmdline_options)

        args_dict = vars(parser.raw_parser.parse_args())
        args_dict['minimal-ohai'] = args_dict.pop('minimal_ohai')
        recipe_file = args_dict.pop('recipe_file')

        # We run one-off command ignoring recipe_file
        command = ([self.locate_binary(self.chef_binary)] +
                   parser.short_arglist(kwargs=args_dict))

        # We execute from a recipe, no execute is given
        if recipe_file and args_dict['execute'] is None:
            # recipe file is the first positional argument
            command.insert(1, recipe_file)

        exit_code = shell.shell_out(command)
        sys.exit(exit_code)


if __name__ == '__main__':
    runner = ChefApplyRunner()
    runner.execute()
