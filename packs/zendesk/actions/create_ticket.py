from lib.zendesk import ZendeskAction

__all__ = [
    'CreateTicketAction'
]


class CreateTicketAction(ZendeskAction):
    def run(self, subject, description):
        return self.create_ticket(subject, description)
