from lib.zendesk import ZendeskAction

__all__ = [
    'UpdateTicketAction'
]


class UpdateTicketAction(ZendeskAction):
    def run(self, ticket_id):
        return True
