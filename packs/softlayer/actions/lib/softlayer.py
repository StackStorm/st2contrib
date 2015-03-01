from libcloud.compute.providers import Provider
from libcloud.compute.providers import get_driver
from st2actions.runners.pythonrunner import Action


class SoftlayerBaseAction(Action):
    def __init__(self, config):
        super(SoftlayerBaseAction, self).__init__(config=config)

    def _get_driver(self):
        cls = get_driver(Provider.SOFTLAYER)
        return cls(self.config['username'], self.config['api_key'])

    def _destroy_instance(self, **kwargs):
        driver = self._get_driver()
        nodes = [node for node in driver.list_nodes() if node.extra['hostname'] == kwargs['name']]
        if len(nodes) == 1:
            self.logger.info("Destroying node {} with remote ID {}".format(kwargs['name'], nodes[0].id))
            return driver.destroy_node(nodes[0])
        else:
            self.logger.error("Node with name {} not found".format(kwargs['name']))
            exit(1)

    def _run_action(self, **kwargs):
        driver = self._get_driver()
        actions = {
            "create_key_pair": driver.create_key_pair,
            "delete_key_pair": driver.delete_key_pair,
            "create_instance": driver.create_node,
            "destroy_instance": self._destroy_instance}

        action = actions[kwargs['action']]
        del kwargs['action']
        # Remove any extra optiona arguments passed
        kwargs = {k: v for k, v in kwargs.iteritems() if v is not None}
        return action(**kwargs)