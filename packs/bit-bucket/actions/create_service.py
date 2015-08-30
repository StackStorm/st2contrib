from lib.action import BitBucketAction


class CreateServiceAction(BitBucketAction):
    def run(self, **kwargs):
        """
        Create a service/hook
        """
        bb = self.perform_request(repo=kwargs['repo'])
        success, result = bb.service.create(
            service=kwargs['service'],
            URL=kwargs['url']
        )
        return result
