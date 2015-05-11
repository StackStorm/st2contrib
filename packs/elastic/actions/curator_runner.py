from easydict import EasyDict
from lib.curator_action import CuratorAction
import logging
import sys

logger = logging.getLogger(__name__)


class CuratorRunner(CuratorAction):

    def run(self, **kwargs):
        self.action = kwargs.pop('action')
        self.config = EasyDict(kwargs)
        self.set_up_logging()
        self.override_timeout()
        self.do_command()
