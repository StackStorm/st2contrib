from lib.actions import YammerAction

__all__ = [
    'ListMessagesAction'
]


class ListMessagesAction(YammerAction):
    def run(self):
        yammer = self.authenticate()
        messages = yammer.messages.all()
        return messages
