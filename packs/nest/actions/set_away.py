from lib import actions


class SetAwayAction(actions.BaseAction):
    def run(self, structure=None):
        if structure:
            s = self._get_structure(structure)
        else:
            s = self._get_default_structure()

        s.away = True
        return s.away
