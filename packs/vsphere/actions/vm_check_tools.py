import eventlet

from pyVmomi import vim

from vmwarelib import inventory
from vmwarelib.actions import BaseAction


class VMCheckTools(BaseAction):

    def run(self, vm_id):
        # convert ids to stubs
        vm = inventory.get_virtualmachine(self.si_content, moid=vm_id)

        # To correctly understand tools status need to consult 3 properties
        # 'powerState' 'ttoolsVersionStatus2' and 'toolsRunningStatus'

        # If VM isn't powered on tools state is meaningless.
        if vm.runtime.powerState != vim.VirtualMachine.PowerState.poweredOn:
            return {"status": vm.runtime.powerState}

        # Tools not installed.
        if vm.guest.toolsVersionStatus2 == \
           vim.vm.GuestInfo.ToolsVersionStatus.guestToolsNotInstalled:
            return {"status": vm.guest.toolsVersionStatus2}

        # Scripts still running therefore wait.
        while vm.guest.toolsRunningStatus != \
                vim.vm.GuestInfo.ToolsRunningStatus.guestToolsRunning:
            eventlet.sleep(1)

        # verify status is running.
        return {"status": vm.guest.toolsRunningStatus}
