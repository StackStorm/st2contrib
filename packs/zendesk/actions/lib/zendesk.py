from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket
from zenpy.lib.api_objects import User

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

    def create_ticket(self, subject, description):
        ticket = Ticket(subject=subject, description=description)

        try:
            created_ticket = self.api.tickets.create(ticket)
            return {'ticket_id': created_ticket.id, 'error': None}
        except Exception as e:
            return {'ticket_id': None, 'error': 'Could not make API request'}

    def search_tickets(self):
        pass

    def update_tickets(self):
        pass

    def close_ticket(self, id):
        pass

