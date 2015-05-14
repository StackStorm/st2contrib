from lib import actions


class SetHomeAction(actions.BaseAction):
    def run(self, structure=None):
        if structure:
            s = self._get_structure(structure)
        else:
            s = self._get_default_structure()

        s.away = False
        return s.away
