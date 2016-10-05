from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket
from zenpy.lib.api_objects import User
from zenpy.lib.api_objects import Comment
from zenpy.lib.exception import RecordNotFoundException
from zenpy.lib.exception import APIException

from st2actions.runners.pythonrunner import Action

__all__ = [
    'ZendeskAction'
]


class ZendeskAction(Action):
    def __init__(self, config):
        super(ZendeskAction, self).__init__(config=config)
        self.email = self.config['email']
        self.token = self.config['api_token']
        self.subdomain = self.config['subdomain']

        self.credentials = {
            'email': self.email,
            'token': self.token,
            'subdomain': self.subdomain
        }

        self.api = Zenpy(**self.credentials)

    def clean_response(self, text):
        return text.replace('\n', ' ').replace('  ', ' ').strip()

    def url_for_ticket(self, ticket):
        return 'https://{}.zendesk.com/agent/tickets/{}'.format(self.subdomain, ticket)

    def create_ticket(self, subject, description):
        ticket = Ticket(subject=subject, description=description)

        try:
            created_ticket_audit = self.api.tickets.create(ticket)
            self.logger.info(description)
            return {
                'ticket_id': created_ticket_audit.ticket.id, 
                'ticket_url': self.url_for_ticket(created_ticket_audit.ticket.id), 
                'subject': self.clean_response(subject),
                'description': self.clean_response(description)
            }
        except Exception as e:
            self.logger.error(e)
            return {'error': 'Could not make API request'}

    def search_tickets(self, query, search_type='ticket', limit=10):
        try:
            query_results = self.api.search(query, type=search_type, sort_by='created_at', sort_order='desc')
            results_clean = map(lambda t: {'ticket_id': t.id, 'ticket_url': self.url_for_ticket(t.id), 'subject': self.clean_response(t.subject), 'description': self.clean_response(t.description)}, list(query_results)[:limit])
            return {'search_results': results_clean}
        except APIException:
            return {'error': 'Could not execute search for query: {}'.format(query)}
        except Exception as e:
            self.logger.error(e)
            return {'error': 'There was an error executing your search'}

    def update_ticket(self, ticket_id, comment_text, public):
        try:
            ticket = self.api.tickets(id=ticket_id)
            ticket.comment = Comment(body=comment_text, public=public)
            self.api.tickets.update(ticket)
            return {'ticket_id': ticket_id, 'body': self.clean_response(comment_text), 'public': public, 'ticket_url': self.url_for_ticket(ticket_id)}
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
                return {'ticket_id': ticket_id, 'ticket_url': self.url_for_ticket(ticket_id), 'status': status}
            except RecordNotFoundException as rnf:
                return {'error': 'Could not find ticket with {ticket_id}'.format(ticket_id=ticket_id)}
            except Exception as e:
                self.logger.error(e)
                return {'error': 'Could not close ticket'}
        else:
            return {'error': 'Invalid status for ticket'}

