from lib.zendesk import ZendeskAction

__all__ = [
    'CloseTicketAction'
]


class CloseTicketAction(ZendeskAction):
    def run(self, ticket_id, status):
        return self.close_ticket(ticket_id, status)
        