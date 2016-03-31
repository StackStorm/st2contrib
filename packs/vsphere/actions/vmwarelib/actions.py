import atexit
import eventlet

from pyVim import connect
from pyVmomi import vim
from st2actions.runners.pythonrunner import Action


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self.si = self._connect()
        self.si_content = self.si.RetrieveContent()

    def _connect(self):
        si = connect.SmartConnect(host=self.config['host'], port=self.config['port'],
                                  user=self.config['user'], pwd=self.config['passwd'])
        atexit.register(connect.Disconnect, si)
        return si

    def _wait_for_task(self, task):
        while task.info.state == vim.TaskInfo.State.running:
            eventlet.sleep(1)
        return task.info.state == vim.TaskInfo.State.success
