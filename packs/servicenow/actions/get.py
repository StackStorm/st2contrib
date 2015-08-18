from lib.actions import BaseAction


class GetAction(BaseAction):
    def run(self, table, query):
        try:
            self.client.table = table
            response = self.client.get(query)
            return response
        except e:
            raise e
