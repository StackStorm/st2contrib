from zenpy import Zenpy

from st2actions.runners.pythonrunner import Action


class ZendeskAction(Action):
    def __init__(self, config):
        super(ZendeskAction, self).__init__(config=config)
        try:
          self.credentials = {
            'email': self.config['email'],
            'token': self.config['api_token'],
            'subdomain': self.config['subdomain']
          }

          self.api = Zenpy(**self.credentials)
        except IndexError as e:
          raise e
