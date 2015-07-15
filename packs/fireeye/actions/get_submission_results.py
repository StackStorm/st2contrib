from lib.actions import BaseAction


class GetSubmissionResults(BaseAction):
    def run(self, query_id):
        url = "/".join(self._url, 'submissions', 'results', query_id)
        r = requests.post(url=url, headers=self._headers)
        r.raise_for_status()
        return r.text
