from lib.action import BaseAction


class GetStatusAction(BaseAction):
    def run(self, item, command):
        return self._get(item, command)
