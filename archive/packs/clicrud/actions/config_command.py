# encoding: utf-8
from st2actions.runners.pythonrunner import Action
from clicrud.device.generic import generic
import sys


class ConfigCommand(Action):

    def run(self, host, command, save):
        self.method = self.config['method']
        self.username = self.config['username']
        self.password = self.config['password']
        self.enable = self.config['enable']

        self.method = self.method.encode('utf-8', 'ignore')
        self.username = self.username.encode('utf-8', 'ignore')
        self.password = self.password.encode('utf-8', 'ignore')
        self.enable = self.enable.encode('utf-8', 'ignore')

        utf8_host = host.encode('utf-8', 'ignore')

        utf8_commands = []

        for cmd in command:
            utf8_commands.append(cmd.encode('utf-8', 'ignore'))

        transport = None

        try:
            transport = generic(host=utf8_host, username=self.username,
                                enable=self.enable, method=self.method,
                                password=self.password)

            return_value = transport.configure(utf8_commands)
            _return_value = str(return_value).encode('utf-8', 'ignore')

            if save is True:
                transport.configure(["write mem"])

            return _return_value
        except Exception as err:
            self.logger.exception('Config command threw an exception')
            self.logger.error(err)
            sys.exit(2)
        finally:
            if transport:
                transport.close()
