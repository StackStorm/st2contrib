from easydict import EasyDict
from lib.curator_action import CuratorAction
import logging
import sys

logger = logging.getLogger(__name__)


class CuratorRunner(CuratorAction):

    def run(self, **kwargs):
        self.action = kwargs.pop('action')
        timeout = kwargs.pop('operation_timeout')
        self.config = EasyDict(kwargs)
        self.config['operation_timeout'] = int(timeout)
        self.set_up_logging()
        self.do_command()
