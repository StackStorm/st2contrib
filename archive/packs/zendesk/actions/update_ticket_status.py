from lib.zendesk import ZendeskAction

__all__ = [
    'UpdateTicketStatusAction'
]


class UpdateTicketStatusAction(ZendeskAction):
    def run(self, ticket_id, status):
        return self.update_ticket_status(ticket_id, status)
