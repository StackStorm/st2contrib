from lib.actions import BaseAction


class GetAction(BaseAction):
    def run(self, table, query):
        self.client.table = table
        response = self.client.get(query)
        return response
