from lib.actions import YammerAction

__all__ = [
    'DeleteGroupAction'
]


class DeleteGroupAction(YammerAction):
    def run(self, id=None):
        yammer = self.authenticate()
        job = yammer.groups.delete(id)
        return job
