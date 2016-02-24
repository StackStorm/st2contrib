from lib import actions
from libcloud.compute.drivers.dimensiondata import DimensionDataNetwork

__all__ = [
    'DeleteNetworkAction',
]


class DeleteNetworkAction(actions.BaseAction):

    def run(self, **kwargs):
        action = kwargs['action']
        del kwargs['action']
        region = kwargs['region']
        del kwargs['region']
        network_id = kwargs['network_id']
        del kwargs['network_id']
        driver = self._get_compute_driver(region)
        network = DimensionDataNetwork(
            id=network_id,
            name=None,
            description=None,
            location=None,
            private_net=None,
            multicast=None,
            status=None
        )
        kwargs['network'] = network
        return self._do_function(driver, action, **kwargs)
