from lib.actions import YammerAction

__all__ = [
    'LikeMessageAction'
]


class LikeMessageAction(YammerAction):
    def run(self, message_id):
        yammer = self.authenticate()
        messages = yammer.messages.like(message_id)
        return messages
