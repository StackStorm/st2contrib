from lib.action import BitBucketAction


class CreteSshKeyAction(BitBucketAction):
    def run(self, ssh_key, label):
        """
        Creat a SSH keys in bitbucket account
        """
        bb = self._get_client()
        success, result = bb.ssh.create(key=ssh_key, label=label)
        return success, result
