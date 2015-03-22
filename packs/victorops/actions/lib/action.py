from st2actions.runners.pythonrunner import Action


class VictorOpsAction(Action):
    def __init__(self, config):
        super(VictorOpsAction, self).__init__(config)
        self.url = "{0}/{1}/{2}".format(self.config['url'], self.config['api_ke
                                        y'],self.config['routing_key'])
