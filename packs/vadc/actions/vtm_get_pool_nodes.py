#! /usr/bin/python

from st2actions.runners.pythonrunner import Action
from lib.vadc import Vtm


class VtmGetPoolNodes(Action):

    def run(self, vtm, pool):

        vtm = Vtm(self.config, self.logger, vtm)
        result = vtm.getPoolNodes(pool)
        return result
