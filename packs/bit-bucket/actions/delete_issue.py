from lib.action import BitBucketAction


class DeleteIssueAction(BitBucketAction):
    def run(self, **kwargs):
        """
        Delete an issue
        """
        bb = self.perform_request(repo=kwargs['repo'])
        for i in kwargs['id']:
            success, result = bb.issue.delete(issue_id=i)
        return result
