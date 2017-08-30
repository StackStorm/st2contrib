#! /usr/bin/python

from st2actions.runners.pythonrunner import Action
from lib.vadc import Bsd


class BsdGetVtmBandwidth(Action):

    def run(self, vtm, stringify):

        bsd = Bsd(self.config, self.logger)
        result = bsd.getBandwidth(vtm, stringify)
        return result
