from lib.action import BitBucketAction


class ListSshKeyAction(BitBucketAction):
    def run(self):
        """
        List all the SSH keys in bitbucket account
        """
        bb = self._get_client()
        succ, result = bb.ssh.all()
        return result
