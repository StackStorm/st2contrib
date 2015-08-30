from lib.action import BitBucketAction


class UpdateServiceAction(BitBucketAction):
    def run(self, **kwargs):
        """
        Update a service/hook
        """
        bb = self.perform_request(repo=kwargs['repo'])
        success, result = bb.service.update(
            service_id=kwargs['id'],
            URL=[kwargs['url']]
        )
        return result
