from lib.actions import YammerAction

__all__ = [
    'ListGroupsAction'
]


class ListGroupsAction(YammerAction):
    def run(self):
        yammer = self.authenticate()
        groups = yammer.groups.all()
        return groups
