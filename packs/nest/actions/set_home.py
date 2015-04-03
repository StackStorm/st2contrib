from lib import actions

class SetHomeAction(actions.BaseAction):
    def run(self, structure=0):
        s = self._get_structure(structure)
        s.away = False
        return s.away

