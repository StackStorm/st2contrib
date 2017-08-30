from urlparse import urljoin

from st2actions.runners.pythonrunner import Action


class OpscenterAction(Action):

    def __init__(self, config=None):
        super(OpscenterAction, self).__init__(config=config)
        self.cluster_id = self.config.get('cluster_id', None)
        self.base_url = self.config.get('opscenter_base_url', None)

    def _get_auth_creds(self):
        pass

    def _get_full_url(self, url_parts):
        base = self.base_url

        if not url_parts:
            return base

        parts = [base]
        parts.extend(url_parts)

        def urljoin_sane(url1, url2):
            if url1.endswith('/'):
                return urljoin(url1, url2)
            else:
                return urljoin(url1 + '/', url2)

        return reduce(urljoin_sane, parts)
