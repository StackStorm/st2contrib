try:
    import libcloud
except ImportError:
    message = ('Missing "apache-libcloud", please install it using pip:\n'
               'pip install apache-libcloud')
    raise ImportError(message)

from libcloud.compute.drivers.dimensiondata import DimensionDataNodeDriver
from libcloud.loadbalancer.drivers.dimensiondata import DimensionDataLBDriver
from dimensiondata_parsers import ResultSets

from st2actions.runners.pythonrunner import Action

__all__ = [
    'BaseAction',
]


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self.resultsets = ResultSets()

    def _get_compute_driver(self, region):
        api_user = self.config['api_user']
        api_pass = self.config['api_password']
        driver = DimensionDataNodeDriver(api_user, api_pass, region=region)
        return driver

    def _get_lb_driver(self, region):
        api_user = self.config['api_user']
        api_pass = self.config['api_password']
        driver = DimensionDataLBDriver(api_user, api_pass, region=region)
        return driver

    def _do_function(self, module, action, **kwargs):
        result = getattr(module, action)(**kwargs)
        return self.resultsets.formatter(result)
