#! /usr/bin/python

from st2actions.runners.pythonrunner import Action
from lib.vadc import Vtm


class VtmMaintenanceMode(Action):

    def run(self, vtm, vserver, rule, enable):

        vtm = Vtm(self.config, self.logger, vtm)
        vtm.enableMaintenance(vserver, rule, enable)
