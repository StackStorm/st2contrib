from lib.action import BitBucketAction


class ArchiveRepoAction(BitBucketAction):
    def run(self, repo):
        """
        Archive a Repository, returns path to
        archived repository
        """
        bb = self._get_client(repo=repo)
        success, archive_path = bb.repository.archive()
        return archive_path
