#!/usr/bin/env python
from lib.icinga2action import Icinga2Action

import sys
import urllib


class Icinga2GetHost(Icinga2Action):

    def run(self, hosts):
        api_suffix = ''
        if hosts:
            if len(hosts) == 1:
                api_suffix = '?host=' + urllib.quote_plus(hosts[0])
            else:
                api_suffix += '?'
                for host in hosts[:-1]:
                    api_suffix += 'hosts=' + urllib.quote_plus(host) + '&'
                api_suffix += 'hosts=' + urllib.quote_plus(hosts[-1])

        self.logger.debug('URL suffix: %s', api_suffix)
        self.set_method('get')
        self.set_path('/objects/hosts' + str(api_suffix))
        self.logger.debug('Action Icinga2GetHost started')
        client = self.get_client()
        client.make_call()
        if self.get_error() == 0:
            return self.get_body()
        else:
            sys.exit(self.get_error())
