from lib.action import BaseAction


class SetStatusAction(BaseAction):
    def run(self, item, command):
        self._put(item, command)
        return {'status': 'ok'}
