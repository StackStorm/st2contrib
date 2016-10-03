from lib.zendesk import ZendeskAction

__all__ = [
    'SearchTicketsAction'
]


class SearchTicketsAction(ZendeskAction):
    def run(self, ticket_id):
        return True
