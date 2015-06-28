from lib import actions


class ToggleAwayAction(actions.BaseAction):
    def run(self, structure=None):
        if structure:
            s = self._get_structure(structure)
        else:
            s = self._get_default_structure()

        s.away = not s.away
        return s.away
