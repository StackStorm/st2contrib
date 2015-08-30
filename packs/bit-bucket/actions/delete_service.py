from lib.action import BitBucketAction


class DeleteServiceAction(BitBucketAction):
    def run(self, **kwargs):
        """
        Delete a service
        """
        bb = self.perform_request(repo=kwargs['repo'])
        for srv in kwargs['id']:
            success, result = bb.service.delete(service_id=srv)
        return result
