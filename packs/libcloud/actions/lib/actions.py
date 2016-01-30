try:
    import libcloud
    libcloud
except ImportError:
    message = ('Missing "apache-libcloud", please install it using pip:\n'
               'pip install apache-libcloud')
    raise ImportError(message)

from libcloud.compute.providers import get_driver as get_compute_driver
from libcloud.storage.providers import get_driver as get_storage_driver
from libcloud.dns.providers import get_driver as get_dns_driver
from libcloud.loadbalancer.providers import get_driver as get_lb_driver
from libcloud.container.providers import get_driver as get_container_driver
from libcloud.compute.base import Node

from libcloud_parsers import ResultSets

from st2actions.runners.pythonrunner import Action

__all__ = [
    'SingleVMAction',
    'BaseAction',
]


class BaseAction(Action):
    api_type = None

    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self.resultsets = ResultSets()

    def _get_driver_for_credentials(self, credentials):
        """
        Retrieve Libcloud provider driver instance for a particular credentials
        set defined in the config.

        :type credentials: ``str``
        """
        provider_config = self.config['credentials'].get(credentials, None)

        if not provider_config:
            raise ValueError(('Invalid credentials set name "%s". Please make'
                              ' sure that credentials set with this name is'
                              ' defined in the config' % (credentials)))

        provider_type = provider_config.get('type', None)
        if provider_type == 'compute':
            get_driver = get_compute_driver
        elif provider_type == 'storage':
            get_driver = get_storage_driver
        elif provider_type == 'dns':
            get_driver = get_dns_driver
        elif provider_type == 'loadbalancer':
            get_driver = get_lb_driver
        elif provider_type == 'container':
            get_driver = get_container_driver
        else:
            raise ValueError('Unsupported type: %s' % (provider_type))

        if provider_type != self.api_type:
            raise ValueError('Expected credentials for "%s", but got credentials for "%s"' %
                             (self.api_type, provider_type))

        cls = get_driver(provider_config['provider'])

        driver_args = [provider_config['api_key'],
                       provider_config['api_secret']]
        driver_kwargs = {}

        if 'region' in provider_config:
            driver_kwargs['region'] = provider_config['region']

        if 'extra_kwargs' in provider_config:
            assert isinstance(provider_config['extra_kwargs'], dict)
            driver_kwargs.update(provider_config['extra_kwargs'])

        driver = cls(*driver_args, **driver_kwargs)
        return driver


class SingleVMAction(BaseAction):
    def _get_node_for_id(self, node_id, driver=None):
        """
        Retrieve Libcloud node instance for the provided node id.
        """
        node = Node(id=node_id, name=None, state=None, public_ips=None,
                    private_ips=None, driver=driver)
        return node
