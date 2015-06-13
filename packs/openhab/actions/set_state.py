from lib.action import BaseAction


class SetStateAction(BaseAction):
    def run(self, item, command):
        self._put(item, command)
        return {'status': 'ok'}
