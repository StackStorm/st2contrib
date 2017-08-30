from lib.actions import YammerAction

__all__ = [
    'DeleteMessageAction'
]


class DeleteMessageAction(YammerAction):
    def run(self, id=None):
        yammer = self.authenticate()
        job = yammer.messages.delete(id)
        return job
