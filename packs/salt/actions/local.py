import json
from requests import Session

from lib.base import SaltAction, logging


class SaltLocal(SaltAction):
    __explicit__ = [
        'cmdmod',
        'event',
        'file',
        'grains',
        'pillar',
        'pkg',
        'saltcloudmod',
        'schedule',
        'service',
        'state',
        'status'
    ]

    def run(self, module, target, expr_form, **kwargs):
        '''
        CLI Examples:

            st2 run salt.local module=test.ping matches='web*'
            st2 run salt.local module=test.ping expr_form=grain target='os:Ubuntu'
        '''
        self.generate_package('local', cmd=module, target=target, expr_form=expr_form, data=kwargs)
        request = self.generate_request()
        request.prepare_body(json.dumps(self.data), None)
        resp = Session().send(request, verify=True)
        return resp.json()
