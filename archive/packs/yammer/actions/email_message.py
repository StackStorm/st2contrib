from lib.actions import YammerAction

__all__ = [
    'EmailMessageAction'
]


class EmailMessageAction(YammerAction):
    def run(self, id=None):
        yammer = self.authenticate()
        job = yammer.messages.email(id)
        return job
