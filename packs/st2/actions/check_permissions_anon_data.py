import sys

from st2actions.runners.pythonrunner import Action


class CheckPermission(Action):
    def run(self, collect_anonymous_data):
        if collect_anonymous_data is True:
            return True
        # No permission therefore exit 1
        sys.exit(1)
