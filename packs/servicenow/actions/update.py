from lib.actions import BaseAction


class UpdateAction(BaseAction):
    def run(self, table, query, payload, sysid):
        self.client.table = table
        response = self.client.update(query, payload, sysid)
        return response
