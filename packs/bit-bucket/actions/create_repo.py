from lib.action import BitBucketAction


class CreateRepoAction(BitBucketAction):
    def run(self, repo):
        """ Create Repository Action """
        bb = self.perform_request()
        success, result = bb.repository.create(repo)
        return result
