from lib.actions import YammerAction

__all__ = [
    'ListUsersAction'
]


class ListUsersAction(YammerAction):
    def run(self, page=None, letter=None,
            sort_by=None, reverse=None):
        yammer = self.authenticate()
        users = yammer.users.all(page=page, letter=letter, sort_by=sort_by,
                                 reverse=reverse)
        return users
