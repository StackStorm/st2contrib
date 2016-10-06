from lib.actions import YammerAction

__all__ = [
    'ListMessagesFromTopicAction'
]


class ListMessagesFromTopicAction(YammerAction):
    def run(self, topic_id):
        yammer = self.authenticate()
        messages = yammer.messages.about_topic(topic_id)
        return messages
