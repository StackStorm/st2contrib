from lib.client import EC2Client


class EC2ConnectMixin(object):
    def __init__(self, config=None):
        self._config = config
        self._ec2 = None

    def setup(self):
        self._ec2 = EC2Client(self._config['region'],
                              self._config['access_key_id'],
                              self._config['secret_access_key'])
        self._ec2.connect()

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass
