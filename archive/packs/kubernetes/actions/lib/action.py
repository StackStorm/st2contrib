from st2actions.runners.pythonrunner import Action


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)
