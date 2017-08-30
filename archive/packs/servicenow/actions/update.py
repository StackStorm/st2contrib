from lib.actions import BaseAction


class UpdateAction(BaseAction):
    def run(self, table, payload, sysid):
        self.client.table = table  # pylint: disable=no-member
        response = self.client.update(payload, sysid)  # pylint: disable=no-member
        return response
