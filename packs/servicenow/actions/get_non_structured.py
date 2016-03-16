from lib.actions import BaseAction


class GetNonStructuredAction(BaseAction):
    def run(self, table, query):
        self.client.table = table  # pylint: disable=no-member
        response = self.client.get(str(query))  # pylint: disable=no-member
        return response
