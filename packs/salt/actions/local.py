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

    def run(self, module, target, expr_form, **kwargs):
        '''
        CLI Examples:

            st2 run salt.local_test.ping matches='web*'
            st2 run salt.local_pkg.install kwargs='{"pkgs":["git","httpd"]}'
        '''
        self.generate_package('local', cmd=module, target=target, expr_form=expr_form)
        request = self.generate_request()
        request.prepare_body(json.dumps(self.data), None)
        resp = Session().send(request, verify=True)
        return resp.json()
