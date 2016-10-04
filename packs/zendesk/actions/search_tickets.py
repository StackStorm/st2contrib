from lib.zendesk import ZendeskAction

__all__ = [
    'SearchTicketsAction'
]


class SearchTicketsAction(ZendeskAction):
    def run(self, ticket_id):
        return self.search_tickets(ticket_id)
