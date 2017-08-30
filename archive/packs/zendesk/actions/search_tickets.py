from lib.zendesk import ZendeskAction

__all__ = [
    'SearchTicketsAction'
]


class SearchTicketsAction(ZendeskAction):
    def run(self, query, limit=10):
        return self.search_tickets(query, limit=limit)
