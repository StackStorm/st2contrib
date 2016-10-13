#! /usr/bin/python

from st2actions.runners.pythonrunner import Action
from lib.vadc import Bsd


class BsdUnlicenseVtm(Action):

    def run(self, vtm):

        bsd = Bsd(self.config, self.logger)
        result = bsd.delVtm(vtm)
        return result
