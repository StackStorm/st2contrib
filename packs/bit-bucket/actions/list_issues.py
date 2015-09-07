from lib.action import BitBucketAction


class ListIssuesAction(BitBucketAction):
    def run(self, repo):
        """
        List Issues of Repository with title
        of the issue its status and reporter
        """
        bb = self._get_client(repo=repo)
        success, result = bb.issue.all()
        return result
