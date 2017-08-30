#!/usr/bin/env python
from lib.icinga2action import Icinga2Action

import sys
import urllib


class Icinga2GetService(Icinga2Action):

    def run(self, services):
        api_suffix = ''
        if services:
            if len(services) == 1:
                api_suffix = '?service=' + urllib.quote_plus(services[0])
            else:
                api_suffix += '?'
                for service in services[:-1]:
                    api_suffix += 'services=' + urllib.quote_plus(service) + '&'
                api_suffix += 'services=' + urllib.quote_plus(services[-1])

        self.logger.debug('URL suffix: %s', api_suffix)
        self.set_method('get')
        self.set_path('/objects/services' + str(api_suffix))
        self.logger.debug('Action Icinga2GetService started')
        client = self.get_client()
        client.make_call()
        if self.get_error() == 0:
            return self.get_body()
        else:
            sys.exit(self.get_error())
