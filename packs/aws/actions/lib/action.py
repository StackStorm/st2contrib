from lib import ec2


class BaseAction(object):

    def __init__(self, config):
        super(BaseAction, self).__init__()
        region = self.config['region']
        access_key_id = self.config['access_key_id']
        secret_access_key = self.config['secret_access_key']
        self.ec2 = ec2.EC2(region, access_key_id, secret_access_key)
