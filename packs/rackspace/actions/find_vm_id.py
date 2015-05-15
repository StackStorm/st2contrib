from lib.action import PyraxBaseAction

__all__ = [
    'FindVMIdAction'
]


class FindVMIdAction(PyraxBaseAction):
    def run(self, name):
        cs = self.pyrax.cloudservers
        vm_id = [vm for vm in cs.servers.list()
                 if vm.name == name][0].id

        return vm_id
