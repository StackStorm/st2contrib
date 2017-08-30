import pyrax

from st2actions.runners.pythonrunner import Action

__all__ = [
    'PyraxBaseAction',
    'BaseVMsAction'
]


class PyraxBaseAction(Action):
    def __init__(self, config):
        super(PyraxBaseAction, self).__init__(config)
        self.pyrax = self._get_client()

    def _get_client(self):
        username = self.config['username']
        api_key = self.config['api_key']

        # Needs to be extracted to per-action
        region = self.config['region'].upper()

        pyrax.set_setting('identity_type', 'rackspace')
        pyrax.set_default_region(region)
        pyrax.set_credentials(username, api_key)

        debug = self.config.get('debug', False)
        if debug:
            pyrax.set_http_debug(True)

        pyrax.cloudservers = pyrax.connect_to_cloudservers(region=region)
        pyrax.cloud_loadbalancers = pyrax.connect_to_cloud_loadbalancers(region=region)
        pyrax.cloud_dns = pyrax.connect_to_cloud_dns(region=region)

        return pyrax


class BaseVMsAction(PyraxBaseAction):
    def _metadata_intersection(self, server, metadata):
        server_metadata = server.get('metadata', {})

        for key, value in metadata.items():
            server_metadata_value = server_metadata.get(key, None)

            if not server_metadata_value or server_metadata_value != value:
                return False

        return True
