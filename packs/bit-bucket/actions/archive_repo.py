from lib.action import BitBucketAction


class ArchiveRepoAction(BitBucketAction):
    def run(self, repo):
        """
        Archive a Repository
        """
        bb = self.perform_request(repo=repo)
        success, archive_path = bb.repository.archive()
        return archive_path
