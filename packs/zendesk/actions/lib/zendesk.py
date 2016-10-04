from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket
from zenpy.lib.api_objects import User
from zenpy.lib.api_objects import Comment
from zenpy.lib.exception import RecordNotFoundException

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
            raise Exception('Missing configuration fields')

    def create_ticket(self, subject, description):
        ticket = Ticket(subject=subject, description=description)

        try:
            created_ticket_audit = self.api.tickets.create(ticket)
            return {'ticket_id': created_ticket_audit.ticket.id, 'ticket_url': created_ticket_audit.ticket.url}
        except Exception as e:
            self.logger.error(e)
            return {'error': 'Could not make API request'}

    def search_tickets(self, ticket_id):
        return {'error': 'Unimplemented'}

    def update_ticket(self, ticket_id, comment_text, public):
        try:
            ticket = self.api.tickets(id=ticket_id)
            ticket.comment = Comment(body=comment_text, public=public)
            self.api.tickets.update(ticket)
            return {'ticket_id': ticket_id, 'body': comment_text, 'public': public}
        except RecordNotFoundException as rnf:
            return {'error': 'Could not find ticket with {ticket_id}'.format(ticket_id=ticket_id)}
        except Exception as e:
            self.logger.error(e)
            return {'error': 'Could not update ticket'}

    def close_ticket(self, ticket_id, status):
        valid_closed_statuses = ['solved', 'closed']
        if status in valid_closed_statuses:
            try:
                ticket = self.api.tickets(id=ticket_id)
                ticket.status = status
                self.api.tickets.update(ticket)
                return {'ticket_id': ticket_id, 'status': status}
            except RecordNotFoundException as rnf:
                return {'error': 'Could not find ticket with {ticket_id}'.format(ticket_id=ticket_id)}
            except Exception as e:
                self.logger.error(e)
                return {'error': 'Could not close ticket'}
        else:
            return {'error': 'Invalid status for ticket'}

