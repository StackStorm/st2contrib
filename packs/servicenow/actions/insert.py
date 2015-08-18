from lib.actions import BaseAction


class InsertAction(BaseAction):
    def run(self, table, payload):
        try:
            self.client.table = table
            response = self.client.insert(payload)
            return response
        except e:
            raise e
