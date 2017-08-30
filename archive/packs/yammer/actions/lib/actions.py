try:
    import yampy
except ImportError:
    message = ('Missing "yampy", please install it using pip:\n'
               'pip install yampy')
    raise ImportError(message)

from st2actions.runners.pythonrunner import Action

__all__ = [
    'YammerAction',
]


class YammerAction(Action):
    def __init__(self, config):
        super(YammerAction, self).__init__(config)
        self.client_id = self.config['client_id']
        self.client_secret = self.config['client_secret']
        self.expected_redirect = self.config['expected_redirect']
        self.authenticator = yampy.Authenticator(
            client_id=self.client_id,
            client_secret=self.client_secret)
        self.access_code = self.config['access_code']
        self.user_info = None
        self.network_info = None

    def authenticate(self):
        access_token = self.authenticator.fetch_access_token(self.access_code)
        return yampy.Yammer(access_token=access_token)
