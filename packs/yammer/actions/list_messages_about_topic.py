from lib.actions import YammerAction

__all__ = [
    'ListMessagesFromTopicAction'
]


class ListMessagesFromTopicAction(YammerAction):
    def run(self, topic_id, older_than_message=None,
            newer_than_message=None, limit=None):
        yammer = self.authenticate()
        messages = yammer.messages.about_topic(
            topic_id,
            older_than=older_than_message,
            newer_than=newer_than_message,
            limit=limit)
        return messages
