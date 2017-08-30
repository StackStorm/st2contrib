#! /usr/bin/python

from st2actions.runners.pythonrunner import Action
from lib.vadc import Bsd


class BsdGetErrors(Action):

    def run(self, stringify):
        bsd = Bsd(self.config, self.logger)
        result = bsd.getErrors(stringify)
        return result
