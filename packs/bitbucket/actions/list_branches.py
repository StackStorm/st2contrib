from lib.action import BitBucketAction


class ListBrachesAction(BitBucketAction):
    def run(self, repo):
        """
        List Braches of Repository with relevant details
        """
        bb = self._get_client(repo=repo)
        success, result = bb.get_branches()
        return result
