#!/usr/bin/env python2.7

import sys
from lib import shellhelpers as shell


def _locate_ohai():
    return 'ohai'

if __name__ == '__main__':
    # this is a workaround since we use run-remote and it
    # passes missing command as None in argv.
    command = ([_locate_ohai()] + [i for i in sys.argv[1:] if i != 'None'])

    sys.exit(shell.shell_out(command))
