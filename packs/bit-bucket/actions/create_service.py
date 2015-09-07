from lib.action import BitBucketAction


class CreateServiceAction(BitBucketAction):
    def run(self, repo, service, url):
        """
        Create a service/hook
        """
        bb = self._get_client(repo=repo)
        success, result = bb.service.create(
            service=service,
            URL=url
        )
        return result
