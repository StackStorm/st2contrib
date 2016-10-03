from zenpy import Zenpy

from st2actions.runners.pythonrunner import Action

__all__ = [
    'ZendeskAction'
]


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

    def create_ticket(subject, description):
        pass

    def search_tickets():
        pass

    def update_tickets():
        pass

    def close_ticket(id):
        pass

