from lib.action import BitBucketAction


class CreateIssueAction(BitBucketAction):
    def run(self, **kwargs):
        """
        Create an issue
        """
        bb = self.perform_request(repo=kwargs['repo'])
        success, result = bb.issue.create(
            title=kwargs['title'],
            content=kwargs['desc'],
            responsible=bb.username,
            status=kwargs['status'],
            kind=kwargs['kind']
        )
        return result
