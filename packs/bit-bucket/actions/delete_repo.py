from lib.action import BitBucketAction


class DeleteRepoAction(BitBucketAction):
    def run(self, repo):
        """ Create Repository Action """
        bb = self._get_client(repo)
        success, result = bb.repository.delete(repo)
        return result
