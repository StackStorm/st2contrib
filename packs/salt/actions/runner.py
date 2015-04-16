import json
from requests import Session

from lib.base import SaltAction


class SaltRunner(SaltAction):

    __explicit__ = [
        'jobs',
        'manage',
        'pillar',
        'mine',
        'network'
    ]

    def run(self, action, **kwargs):
        _cmd = action
        '''
        CLI Examples:

            st2 run salt.runner_jobs.active
            st2 run salt.runner_jobs.list_jobs
        '''
        self.generate_package('runner', cmd=_cmd)
        #if args:
        #    self.data['arg'] = [args]
        #if kwargs:
        #    self.data['kwargs'] = kwargs
        request = self.generate_request()
        request.prepare_body(json.dumps(self.data), None)
        resp = Session().send(request, verify=True)
        return resp.json()
