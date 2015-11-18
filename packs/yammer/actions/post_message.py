from lib.actions import YammerAction

__all__ = [
    'PostMessageAction'
]


class PostMessageAction(YammerAction):
    def run(self, message, group_id, topics, replied_to_id):
        yammer = self.authenticate()
        return yammer.messages.create(
            message, group_id=group_id,
            topics=topics, replied_to_id=replied_to_id)
