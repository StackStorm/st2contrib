#! /usr/bin/python

import requests
import sys
from st2actions.runners.pythonrunner import Action

from lib.vadc import Vtm

class VtmDrainNodes(Action):

    def run(self, vtm, name, nodes, drain):

		vtm = Vtm(self.config, self.logger, vtm)
		vtm.drainNodes(name, nodes, drain)

