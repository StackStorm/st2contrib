from lib.action import BitBucketAction


class DeleteSshKeyAction(BitBucketAction):
    def run(self, key_id):
        """
        Delete SSH key from BitBucket account
        """
        bb = self._get_client()
        succ, res = bb.ssh.delete(key_id=key_id)
        return succ, res
