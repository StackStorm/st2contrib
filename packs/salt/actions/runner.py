import json
from requests import Session

from lib.base import SaltAction


class SaltRunner(SaltAction):

    __explicit__ = [
        'jobs',
        'manage',
        'pillar',
        'network'
    ]

    def run(self, **kwargs):
        _cmd = None
        if '.' not in kwargs['cmd']:
            _cmd = '{0}.{1}'.format(kwargs['action'], kwargs['cmd'])
        else:
            _cmd = kwargs['cmd']
        '''
        CLI Examples:

            st2 run salt.jobs active
            st2 run salt.jobs jobs.list_jobs
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
