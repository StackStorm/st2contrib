#! /usr/bin/python

from st2actions.runners.pythonrunner import Action
from lib.vadc import Bsd


class BsdSetVtmBandwidth(Action):

    def run(self, vtm, bw):

        bsd = Bsd(self.config, self.logger)
        bsd.setBandwidth(vtm, bw)
