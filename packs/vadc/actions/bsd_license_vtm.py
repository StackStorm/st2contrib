#! /usr/bin/python

from st2actions.runners.pythonrunner import Action
from lib.vadc import Bsd


class BsdLicenseVtm(Action):

    def run(self, vtm, password, address, bw, fp):

        bsd = Bsd(self.config, self.logger)
        result = bsd.addVtm(vtm, password, address, bw, fp)
        return result
