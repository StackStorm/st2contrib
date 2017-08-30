from lib.action import BaseAction


class SendCommandAction(BaseAction):
    def run(self, item, command):
        self._post(item, command)
        return {'status': 'ok'}
