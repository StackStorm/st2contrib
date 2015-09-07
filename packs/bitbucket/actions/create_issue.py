from lib.action import BitBucketAction


class CreateIssueAction(BitBucketAction):
    def run(self, repo, title, desc, status, kind):
        """
        Create an issue
        """
        bb = self._get_client(repo=repo)
        print bb.username
        success, result = bb.issue.create(
            title=title,
            content=desc,
            responsible=bb.username,
            status=status,
            kind=kind
        )
        return result
