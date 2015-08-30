from lib.action import BitBucketAction


class ListServicesAction(BitBucketAction):
    def run(self, repo):
        """
        List Services associated with Repository
        """
        bb = self.perform_request(repo=repo)
        success, result = bb.service.all()
        return result
