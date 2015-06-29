from lib import actions


class GetProgress(actions.BaseAction):
    def run(self, uuid, raw=False):

        response = self.client.get_progress(uuid, raw)
        return response
