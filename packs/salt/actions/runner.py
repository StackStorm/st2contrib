import json
from requests import Session

from lib.base import SaltAction


class SaltRunner(SaltAction):

    def run(self, cmd, args=None, **kwargs):
        '''
        CLI Examples:

            st2 run salt.runner manage.down
            st2 run salt.runner manage.down removekeys=True
        '''
        self.generate_package('runner', cmd=cmd)
        if args:
            self.data['arg'] = [args]
        if kwargs:
            self.data['kwargs'] = kwargs
        request = self.generate_request()
        request.prepare_body(json.dumps(self.data), None)
        resp = Session().send(request, verify=True)
        return resp.json()
