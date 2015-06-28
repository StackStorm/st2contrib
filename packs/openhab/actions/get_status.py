from lib.action import BaseAction


class GetStatusAction(BaseAction):
    def run(self, item):
        return self._get(item)
