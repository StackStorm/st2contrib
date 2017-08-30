from lib.zendesk import ZendeskAction

__all__ = [
    'UpdateTicketAction'
]


class UpdateTicketAction(ZendeskAction):
    def run(self, ticket_id, comment_text, public=False):
        return self.update_ticket(ticket_id, comment_text, public)
