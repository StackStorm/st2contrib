import os
import sys
import subprocess
from st2common.util.shell import quote_unix

__all__ = [
    'AnsibleBaseRunner'
]


class AnsibleBaseRunner(object):
    """
    Base class for all Ansible Runners
    """
    BINARY_NAME = None

    def __init__(self, args):
        """
        :param args: Input command line arguments
        :type args: ``list``
        """
        self.args = args[1:]

    def execute(self):
        """
        Execute the command.
        Exit with 0 error code on success or 1 on error.
        TODO: Streaming output as it appears
        """
        if subprocess.call(self.cmd) is not 0:
            sys.stderr.write('Executed command "%s"\n' % ' '.join(self.cmd))
            sys.exit(1)

    @property
    def cmd(self):
        """
        Get full command line with parameters to execute.

        NB! Don't shell-escape `args` parameter, or such commands would fail:
        $ ansible all --module-name=shell --args='echo 123'

        :return: Command line
        :rtype: ``list``
        """
        arguments = self._apply_replacements(self.args)
        quote_specific = lambda a: a if a.startswith('--args') else quote_unix(a)
        return map(quote_specific, [self.binary] + arguments)

    @staticmethod
    def _apply_replacements(args):
        """
        Apply replacements for input list of arguments.

        :param args:
        :type args: ``list``
        :return: New arguments
        :rtype: ``list``
        """
        rules = {
            '--verbose=v': '-v',
            '--verbose=vv': '-vv',
            '--verbose=vvv': '-vvv',
            '--verbose=vvvv': '-vvvv',
        }
        return map(lambda a: rules[a] if a in rules else a, args)

    @property
    def binary(self):
        """
        Get full path to executable binary located in pack virtualenv.

        :return: Full path to executable binary.
        :rtype: ``str``
        """
        if not self.BINARY_NAME:
            sys.stderr.write('Ansible binary file name was not specified')
            sys.exit(1)
        # return os.path.join(get_sandbox_virtualenv_path(pack='ansible'), 'bin', self._BINARY_NAME)
        path = os.path.join('/opt/stackstorm/virtualenvs/ansible/bin', self.BINARY_NAME)
        if not os.path.isfile(path):
            sys.stderr.write('Ansible binary doesnt exist. Is it installed?')
            sys.exit(1)

        return path
