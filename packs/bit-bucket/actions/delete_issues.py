from lib.action import BitBucketAction


class DeleteIssueAction(BitBucketAction):
    def run(self, repo, ids):
        """
        Delete an issue
        """
        bb = self._get_client(repo=repo)
        for i in ids:
            success, result = bb.issue.delete(issue_id=i)
        return result
