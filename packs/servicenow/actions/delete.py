from lib.actions import BaseAction


class DeleteAction(BaseAction):
    def run(self, table, sysid):
        self.client.table = table
        response = self.client.delete(sysid)
        return response
