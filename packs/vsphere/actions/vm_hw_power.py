import eventlet
from pyVmomi import vim

from vmwarelib import inventory
from vmwarelib import checkinputs
from vmwarelib.actions import BaseAction


class VMPowerOn(BaseAction):

    def run(self, vm_id, vm_name, power_onoff):
        # check I have information to find a VM
        checkinputs.vm_identifier(vm_id, vm_name)
        # convert ids to stubs
        vm = inventory.get_virtualmachine(self.si_content,
                                          moid=vm_id, name=vm_name)
        if not vm:
            raise Exception('Error: Unable to find VM')
        if power_onoff == "poweroff":
            task = vm.PowerOffVM_Task()
        else:
            task = vm.PowerOnVM_Task()
        while task.info.state == vim.TaskInfo.State.running:
            eventlet.sleep(1)
        return {'state': str(task.info.state)}
