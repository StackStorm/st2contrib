from lib.sensu import SensuAction

__all__ = [
    'UnsilenceAction'
]


class UnsilenceAction(SensuAction):
    def run(self, check, client):
        path = 'silence/{}'.format(client)
        if check:
            path = "{}/{}".format(path, check)

        return self.api.delete_stash(path)
