from lib.softlayer import SoftlayerBaseAction


class SoftlayerDeleteInstance(SoftlayerBaseAction):
    def run(self, name):
        driver = self._get_driver()
        # go from name to Node Object
        node = [n for n in driver.list_nodes() if n.extra['hostname'] == name][0]
        # destroy the node
        self.logger.info('Destroying node...')
        node = driver.destroy_node(node)
        self.logger.info('Node successfully destroyed: {}'.format(node))
        return