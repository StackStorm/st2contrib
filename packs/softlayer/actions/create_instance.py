from lib.softlayer import SoftlayerBaseAction


class SoftlayerCreateInstance(SoftlayerBaseAction):
    def run(self, name, datacenter, os="DEBIAN_LATEST", domain="example.com", cpus=1, ram=2048,
            disk=100, bandwidth=10, local_disk=True, keyname=None):
        driver = self._get_driver()
        # build the params list to pass to create_node with the proper kwargs
        create_params = {"name": name, "ex_datacenter": datacenter,
                         self.st2_to_libcloud['os']: os,
                         self.st2_to_libcloud['domain']: domain,
                         self.st2_to_libcloud['cpus']: cpus,
                         self.st2_to_libcloud['disk']: disk,
                         self.st2_to_libcloud['ram']: ram,
                         self.st2_to_libcloud['bandwidth']: bandwidth,
                         self.st2_to_libcloud['local_disk']: local_disk}

        if keyname is not None:
            create_params[self.st2_to_libcloud['keyname']] = keyname
        # create the node
        self.logger.info('Creating node...')
        node = driver.create_node(**create_params)
        self.logger.info('Node successfully created: {}'.format(node))
        return node
