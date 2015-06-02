from lib import actions

class GetProgress(actions.BaseAction):
    def run(self, uuid, raw=False):

        client = self.client
        response = client.get_progress(uuid, raw)
        return response
