from lib.actions import BaseAction


class GetAction(BaseAction):
    def run(self, table, query):
        self.client.table = table  # pylint: disable=no-member
        response = self.client.get(query)  # pylint: disable=no-member
        return response
