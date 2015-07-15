from lib.actions import BaseAction


class GetSubmissionStatus(BaseAction):
    def run(self, query_id):
        url = "/".join(self._url, 'submissions', 'status', query_id)
        r = requests.post(url=url, headers=self._headers)
        r.raise_for_status()
        return r.text
