import os
import re

from st2common.util.shell import run_command
from st2actions.runners.pythonrunner import Action

__all__ = [
    'JAR_PATH'
]

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
JAR_PATH = os.path.join(CURRENT_DIR, '../extern/cmdline-jmxclient/cmdline-jmxclient-0.10.3.jar')
JAR_PATH = os.path.abspath(JAR_PATH)


class InvokeMBeanMethodAction(Action):
    def run(self, hostname, port, bean_name, command, arguments=None,
            username=None, password=None):
        args = self._get_args(hostname=hostname, port=port,
                              bean_name=bean_name, command=command,
                              arguments=arguments, username=username,
                              password=password)

        command = ' '.join(args)
        self.logger.debug('Running command: "%s"' % (command))
        exit_code, stdout, stderr = run_command(cmd=args)

        if exit_code != 0:
            msg = 'Failed to invoke command: %s' % (stderr)
            raise Exception(msg)

        if re.match('.*Operation .*? not found.*', stderr):
            msg = 'Failed to invoke command: %s' % (stderr)
            raise Exception(msg)

        if 'Passed param count does not match signature count' in stderr:
            msg = 'Failed to invoke command: %s' % (stderr)
            raise Exception(msg)

        self.logger.debug('Command successfully finished. Output: %s' % (stdout))
        return True

    def _get_args(self, hostname, port, bean_name, command, arguments=None,
                  username=None, password=None):

        credentials = []
        if username:
            credentials.append(username)

        if password:
            credentials.append(password)

        if credentials:
            credentials = ':'.join(credentials)
        else:
            credentials = '-'

        url = '%s:%s' % (hostname, port)

        if arguments:
            arguments = ','.join(arguments)
            command = '%s=%s' % (command, arguments)
        else:
            command = command

        args = [
            'java',
            '-jar',
            JAR_PATH,
            credentials,
            url,
            bean_name,
            command
        ]

        return args
