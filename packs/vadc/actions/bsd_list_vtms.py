#! /usr/bin/python

import requests
import sys
from st2actions.runners.pythonrunner import Action

from lib.vadc import Bsd

class BsdListVtms(Action):

    def run(self, full, deleted, stringify):

      bsd = Bsd(self.config, self.logger)
      result = bsd.listVtms(full, deleted, stringify)
      return result 

