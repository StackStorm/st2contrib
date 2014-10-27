class BaseAction(object):

    def __init__(self, config):
        super(BaseAction, self).__init__()
        self.region = self.config['region']
        self.access_key_id = self.config['access_key_id']
        self.secret_access_key = self.config['secret_access_key']
