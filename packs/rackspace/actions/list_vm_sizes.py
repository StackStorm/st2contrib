from lib.action import PyraxBaseAction

__all__ = [
    'ListVMSizes'
]


class ListVMSizes(PyraxBaseAction):
    def run(self):
        cs = self.pyrax.cloudservers
        flavors = cs.list_flavors()
        result = {}

        for flavor in flavors:
            result[flavor.id] = {
                'name': flavor.name,
                'ram': flavor.ram,
                'disk': flavor.disk,
                'vcpus': flavor.vcpus
            }

        return result
