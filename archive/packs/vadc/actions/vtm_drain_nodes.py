#! /usr/bin/python

from st2actions.runners.pythonrunner import Action
from lib.vadc import Vtm


class VtmDrainNodes(Action):

    def run(self, vtm, pool, nodes, drain):

        vtm = Vtm(self.config, self.logger, vtm)
        vtm.drainNodes(pool, nodes, drain)
