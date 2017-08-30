#! /usr/bin/python

from st2actions.runners.pythonrunner import Action
from lib.vadc import Vtm


class VtmDisableSslEncryption(Action):

    def run(self, vtm, name, verify):

        vtm = Vtm(self.config, self.logger, vtm)
        vtm.enableSSLEncryption(name, False, verify)
