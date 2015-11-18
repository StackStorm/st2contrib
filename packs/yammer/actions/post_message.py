from lib.actions import YammerAction

__all__ = [
    'PostMessageAction'
]


class PostMessageAction(YammerAction):
    def run(self, message, group_id, topics=None, replied_to_id=None, direct_to_id=None):
        yammer = self.authenticate()
        return yammer.messages.create(
            message, group_id=group_id,
            topics=topics, replied_to_id=replied_to_id,
            direct_to_id=direct_to_id)
