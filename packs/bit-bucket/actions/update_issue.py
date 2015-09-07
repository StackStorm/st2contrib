from lib.action import BitBucketAction


class UpdateIssueAction(BitBucketAction):
    def run(self, repo, id, desc):
        """
        Update an issue
        """
        bb = self._get_client(repo=repo)
        success, result = bb.issue.update(
            issue_id=id,
            content=desc
        )
        return result
