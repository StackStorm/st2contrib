from lib.action import BitBucketAction


class UpdateServiceAction(BitBucketAction):
    def run(self, repo, id, url):
        """
        Update a service/hook
        """
        bb = self._get_client(repo=repo)
        success, result = bb.service.update(
            service_id=id,
            URL=url
        )
        return result
