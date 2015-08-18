from lib.actions import BaseAction


class InsertAction(BaseAction):
    def run(self, table, payload):
        self.client.table = table
        response = self.client.insert(payload)
        return response
