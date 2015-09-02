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
        repository = []
        bb = self.perform_request()
        success, repos = bb.repository.all()
        for repo in sorted(repos):
            repository.append(
                {repo['name']: {'state': repo['state'],
                                'last_updated_at': repo['last_updated'],
                                'is_private': repo['is_private']}})
        return repository
