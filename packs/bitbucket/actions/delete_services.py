from lib.action import BitBucketAction


class DeleteServiceAction(BitBucketAction):
    def run(self, repo, ids):
        """
        Delete a service
        """
        bb = self._get_client(repo=repo)
        for srv in ids:
            success, result = bb.service.delete(service_id=srv)
        return result
