from lib import actions


class GetResultSummary(actions.BaseAction):
    def run(self, uuid, raw=False, requested_format='json',
            score_only=False, verify=True):

        response = self.client.get_result_summary(uuid, raw, requested_format,
                                                  score_only, verify)

        return response
