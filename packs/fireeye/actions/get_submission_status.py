from lib.actions import BaseAction


class GetSubmissionStatus(BaseAction):
    def run(self, query_id):
        endpoint = "/".join(['submissions', 'status', query_id])
        response = self._api_get(endpoint)
        return response
