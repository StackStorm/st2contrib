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

    def run(self, module, **kwargs):
        self.verify_ssl = self.config.get('verify_ssl', True)
        _cmd = module
        '''
        CLI Examples:

            st2 run salt.runner_jobs.active
            st2 run salt.runner_jobs.list_jobs
        '''
        self.generate_package('runner', cmd=_cmd)
        if kwargs.get('kwargs', None) is not None:
            self.data.update(kwargs['kwargs'])
        request = self.generate_request()
        request.prepare_body(json.dumps(self.data), None)
        resp = Session().send(request, verify=self.verify_ssl)
        return resp.json()
