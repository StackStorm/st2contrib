from lib.softlayer import SoftlayerBaseAction


class SoftlayerCreateKeypair(SoftlayerBaseAction):
    def run(self, name, size=4096):
        driver = self._get_driver()
        self.logger.info('Creating keypair...')
        keypair = driver.create_key_pair(name, size)
        self.logger.info('Keypair successfully created: {}'.format(keypair))
        return
