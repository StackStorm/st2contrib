from lib.actions import YammerAction

__all__ = [
    'ListMessagesFromUserAction'
]


class ListMessagesFromUserAction(YammerAction):
    def run(self, user_id, older_than_message=None,
            newer_than_message=None, limit=None):
        yammer = self.authenticate()
        messages = yammer.messages.from_user(
            user_id,
            older_than=older_than_message,
            newer_than=newer_than_message,
            limit=limit)
        return messages
