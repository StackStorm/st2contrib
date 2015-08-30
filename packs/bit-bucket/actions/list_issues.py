from lib.action import BitBucketAction


class ListIssuesAction(BitBucketAction):
    def run(self, repo):
        """
        List Issues of Repository with title
        of the issue its status and reporter
        """
        bb = self.perform_request(repo=repo)
        success, result = bb.issue.all()
        issues = {}
        for i in range(result['count']):
            issues[result['issues'][i]['title']] = {
                'status': result['issues'][i]['status'],
                'reporter': result['issues'][i]['reported_by']['username'],
                'issue_id': result['issues'][i]['local_id']
            }
        return issues
