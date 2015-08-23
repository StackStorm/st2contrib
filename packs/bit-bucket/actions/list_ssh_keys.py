from lib.action import BitBucketAction


class ListSshKeyAction(BitBucketAction):
    def run(self, repo):
        """
        List all the SSH keys in bitbucket account
        """
        bb = self.perform_request(repo=repo)
        succ, res = bb.ssh.all()
        data = {}
        for i in range(len(res)):
            data[res[i]['pk']] = res[i]['label']
        return data
