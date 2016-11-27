from lib.sensu import SensuAction

__all__ = [
    'SilenceAction'
]


class SilenceAction(SensuAction):
    def run(self, check, client, expiration, message):
        path = 'silence/{}'.format(client)
        if check:
            path = "{}/{}".format(path, check)

        payload = {}
        payload['message'] = message

        if expiration:
            payload['expire'] = expiration

        return self.api.create_stash(payload, path)
