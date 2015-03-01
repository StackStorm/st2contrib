from lib import softlayer


class Softlayer(softlayer.SoftlayerBaseAction):
    def run(self, **kwargs):
        return self._run_action(**kwargs)
