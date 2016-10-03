from lib.zendesk import ZendeskAction

__all__ = [
    'CloseTicketAction'
]


class CloseTicketAction(ZendeskAction):
    def run(self, ticket_id):
        return True
        