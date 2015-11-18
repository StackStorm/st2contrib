from lib.actions import YammerAction

__all__ = [
    'ListMessagesFromUserAction'
]


class ListMessagesFromUserAction(YammerAction):
    def run(self, user_id):
        yammer = self.authenticate()
        messages = yammer.messages.from_user(user_id)
        return messages
