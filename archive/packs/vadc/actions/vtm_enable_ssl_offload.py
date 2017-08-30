#! /usr/bin/python

from st2actions.runners.pythonrunner import Action
from lib.vadc import Vtm


class VtmEnableSslOffload(Action):

    def run(self, vtm, name, cert, xproto, headers):

        vtm = Vtm(self.config, self.logger, vtm)
        vtm.enableSSLOffload(name, cert, True, xproto, headers)
