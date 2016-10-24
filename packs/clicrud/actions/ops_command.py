# encoding: utf-8
from st2actions.runners.pythonrunner import Action
from clicrud.device.generic import generic
import sys


class OPSCommand(Action):

    def run(self, host, command):
        self.method = self.config['method']
        self.username = self.config['username']
        self.password = self.config['password']
        self.enable = self.config['enable']

        self.method = self.method.encode('utf-8', 'ignore')
        self.username = self.username.encode('utf-8', 'ignore')
        self.password = self.password.encode('utf-8', 'ignore')
        self.enable = self.enable.encode('utf-8', 'ignore')

        utf8_command = command.encode('utf-8', 'ignore')
        utf8_host = host.encode('utf-8', 'ignore')

        try:

            transport = generic(host=utf8_host, username=self.username,
                                enable=self.enable, method=self.method,
                                password=self.password)

            return_value = transport.read(utf8_command, return_type="string")
            return_value = unicode(return_value, "utf-8")
            transport.close()
            return return_value
        except Exception, err:
            self.logger.info('FUBARd')
            self.logger.info(err)
            sys.exit(2)
