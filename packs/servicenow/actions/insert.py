from lib.actions import BaseAction


class InsertAction(BaseAction):
    def run(self, table, payload):
        self.client.table = table  # pylint: disable=no-member
        response = self.client.insert(payload)  # pylint: disable=no-member
        return response
