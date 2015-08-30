from lib.action import BitBucketAction


class UpdateIssueAction(BitBucketAction):
    def run(self, **kwargs):
        """
        Update an issue
        """
        bb = self.perform_request(repo=kwargs['repo'])
        success, result = bb.issue.update(
            issue_id=kwargs['id'],
            content=[kwargs['desc']]
        )
        return result
