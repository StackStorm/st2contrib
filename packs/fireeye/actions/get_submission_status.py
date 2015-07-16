from lib.actions import BaseAction


class GetSubmissionStatus(BaseAction):
    def run(self, query_id):
        url = "/".join([self._api_root, 'submissions', 'status', query_id])
        r = requests.get(url=url, headers=self._headers)
        r.raise_for_status()
        return r.text
