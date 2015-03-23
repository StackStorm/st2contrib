from lib import actions

class SetAwayAction(actions.BaseAction):
    def run(self, structure):
        s = self._get_structure(structure)
        s.away = True
        return s.away

