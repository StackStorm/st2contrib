from lib.action import BaseAction


class SendCommandAction(BaseAction):
    def run(self, device_type=None, device_id=None, command=None,
            value=None, mode=None):
        params = {}
        url = "/{}/{}".format(device_type, device_id)

        if command:
            params['command'] = command
        if value:
            params['value'] = value
        if mode:
            params['mode'] = mode

        return self._put(url, params)
