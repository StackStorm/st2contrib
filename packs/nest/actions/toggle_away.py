from lib import actions

class ToggleAwayAction(actions.BaseAction):
    def run(self, structure=0):
        s = self._get_structure(structure)
        s.away = not s.away
        return s.away
