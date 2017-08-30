from lib.action import BaseAction


class SetStateAction(BaseAction):
    def run(self, item, state):
        self._put(item, state)
        return {'status': 'ok'}
