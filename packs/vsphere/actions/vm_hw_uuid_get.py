from vmwarelib import inventory
from vmwarelib.actions import BaseAction


class GetVMUUID(BaseAction):

    def run(self, vms):
        results = []
        for vm in vms:
            vm = inventory.get_virtualmachine(self.si_content, name=vm)
            if vm:
                results.append({vm.name: vm.summary.config.uuid})
        return results
