#!/usr/bin/env python
from lib.icinga2action import Icinga2Action
import sys


class Icinga2GetStatus(Icinga2Action):

    def run(self):
        self.set_method('get')
        self.set_path('/status')
        self.logger.debug('Action Icinga2GetStatus started')
        client = self.get_client()
        client.make_call()
        if self.get_error() == 0:
            return self.get_body()
        else:
            sys.exit(self.get_error())
