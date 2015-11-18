from lib.actions import YammerAction

__all__ = [
    'ListMessagesMyFeedAction'
]


class ListMessagesMyFeedAction(YammerAction):
    def run(self):
        yammer = self.authenticate()
        messages = yammer.messages.from_my_feed()
        return messages
