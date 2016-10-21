#! /usr/bin/python

from st2actions.runners.pythonrunner import Action
from lib.vadc import Vtm


class VtmAddPool(Action):

    def run(self, vtm, name, nodes, algorithm, persistence, monitors):

        vtm = Vtm(self.config, self.logger, vtm)
        vtm.addPool(name, nodes, algorithm, persistence, monitors)
