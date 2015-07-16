from lib.actions import BaseAction


class GetSubmissionResults(BaseAction):
    def run(self, query_id):
        url = "/".join([self._api_root, 'submissions', 'results', query_id])
        r = requests.get(url=url, headers=self._headers)
        r.raise_for_status()
        return r.text
