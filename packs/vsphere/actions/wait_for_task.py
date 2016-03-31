import eventlet

from pyVmomi import vim

from vmwarelib import inventory
from vmwarelib.actions import BaseAction


class WaitTask(BaseAction):

    def run(self, task_id):
        # convert ids to stubs
        task = inventory.get_task(self.si_content, moid=task_id)
        while task.info.state == vim.TaskInfo.State.running:
            eventlet.sleep(1)
        result, error = None, None
        if task.info.state == vim.TaskInfo.State.success:
            result = task.info.result
        else:
            error = task.info.error
        return {'result': result, 'error': error}
