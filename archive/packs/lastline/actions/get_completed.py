from lib import actions


class GetCompleted(actions.BaseAction):
    def run(self, after, before=None, raw=False,
            verify=True, include_score=False):

        response = self.client.get_completed(after, before, raw,
                                             verify, include_score)

        return response
