from lib.actions import YammerAction

__all__ = [
    'ListMessagesAction'
]


class ListMessagesAction(YammerAction):
    def run(self, older_than_message=None,
            newer_than_message=None, limit=None):
        yammer = self.authenticate()
        messages = yammer.messages.all(older_than=older_than_message,
                                       newer_than=newer_than_message,
                                       limit=limit)
        return messages
