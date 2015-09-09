from lib.actions import BaseAction


class DeleteAction(BaseAction):
    def run(self, table, sysid):
        self.client.table = table  # pylint: disable=no-member
        response = self.client.delete(sysid)  # pylint: disable=no-member
        return response
