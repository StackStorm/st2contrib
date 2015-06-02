from lib import actions

class GetCompleted(actions.BaseAction):
    def run(self, after, before=None, raw=False,
            verify=True, include_score=False):

        client = self.client
        response = client.get_completed(after, before, raw,
                                        verify, include_score)

        return response
