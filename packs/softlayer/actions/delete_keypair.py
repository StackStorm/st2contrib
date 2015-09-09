from lib.softlayer import SoftlayerBaseAction


class SoftlayerDeleteKeypair(SoftlayerBaseAction):
    def run(self, name):
        driver = self._get_driver()
        self.logger.info('Deleting keypair...')
        keypair = driver.delete_key_pair(name)
        self.logger.info('Keypair successfully deleted: {}'.format(keypair))
        return
