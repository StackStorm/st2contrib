import json
from requests import Session

from lib.base import SaltAction


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

    def run(self, module, target, expr_form, args, **kwargs):
        self.verify_ssl = self.config.get('verify_ssl', True)
        '''
        CLI Examples:

            st2 run salt.local module=test.ping matches='web*'
            st2 run salt.local module=test.ping expr_form=grain target='os:Ubuntu'
        '''
        self.generate_package('local',
                              cmd=module,
                              args=list(args),
                              target=target,
                              expr_form=expr_form,
                              data=kwargs)
        request = self.generate_request()
        self.logger.info('[salt] Request generated')
        request.prepare_body(json.dumps(self.data), None)
        self.logger.info('[salt] Preparing to send')
        resp = Session().send(request, verify=self.verify_ssl)
        return resp.json()
