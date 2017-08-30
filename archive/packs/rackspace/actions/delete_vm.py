from lib.action import PyraxBaseAction

__all__ = [
    'DeleteVMAction'
]


class DeleteVMAction(PyraxBaseAction):
    def run(self, vm_id):
        cs = self.pyrax.cloudservers

        server = cs.servers.get(vm_id)
        server.delete()

        return True
