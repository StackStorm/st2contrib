from lib.actions import BaseAction


class UpdateAction(BaseAction):
    def run(self, table, query, payload, sysid):
        self.client.table = table  # pylint: disable=no-member
        response = self.client.update(query, payload, sysid)  # pylint: disable=no-member
        return response
