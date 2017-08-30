from lib.actions import BaseAction


class GetSubmissionResults(BaseAction):
    def run(self, query_id):
        endpoint = "/".join(['submissions', 'results', query_id])
        response = self._api_get(endpoint)
        return response
