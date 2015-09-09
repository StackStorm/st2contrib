from lib import action


class CurrentStateAction(action.BaseAction):
    def run(self):
        return self.hue.state
