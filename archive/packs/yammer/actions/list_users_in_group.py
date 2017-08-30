from lib.actions import YammerAction

__all__ = [
    'ListUsersInGroupAction'
]


class ListUsersInGroupAction(YammerAction):
    def run(self, group_id, page=None):
        yammer = self.authenticate()
        users = yammer.users.in_group(group_id, page=page)
        return users
