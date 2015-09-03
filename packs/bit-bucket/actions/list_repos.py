from lib.action import BitBucketAction


class ListReposAction(BitBucketAction):
    def run(self):
        """
        Listing repositories for a user.It assumes
        that you have already places the name and
        password in config file. It returns repo's
        name, its state and private status(returns
        True if its private, False otherwise)
        """
        bb = self._get_client()
        success, repos = bb.repository.all()
        return repos
