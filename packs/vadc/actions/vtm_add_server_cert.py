#! /usr/bin/python

from st2actions.runners.pythonrunner import Action
from lib.vadc import Vtm


class VtmAddServerCert(Action):

    def run(self, vtm, name, public, private):

        vtm = Vtm(self.config, self.logger, vtm)
        vtm.addServerCert(name, public, private)
