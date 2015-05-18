import os
import sys
import subprocess
import shell

__all__ = [
    'AnsibleBaseRunner'
]


class AnsibleBaseRunner(object):
    """
    Base class for all Ansible Runners
    """
    BINARY_NAME = None
    EXCLUDE_ESCAPE = None
    REPLACEMENT_RULES = None

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
        """
        # TODO: Stream output as it appears
        if subprocess.call(self.cmd) is not 0:
            sys.stderr.write('Executed command "%s"\n' % ' '.join(self.cmd))
            sys.exit(1)

    @property
    @shell.escape_args('EXCLUDE_ESCAPE')
    @shell.replace_args('REPLACEMENT_RULES')
    def cmd(self):
        """
        Get full command line as list.

        :return: Command line.
        :rtype: ``list``
        """
        return [self.binary] + self.args

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
