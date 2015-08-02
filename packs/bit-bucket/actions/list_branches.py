from lib.action import BitBucketAction


class ListBrachesAction(BitBucketAction):
    def run(self, repo):
        """
        List Braches of Repository with author names and message
        """
        bb = self.perform_request(repo=repo)
        success, result = bb.get_branches()
        branches = {}
        for key, value in result.iteritems():
            branches[key] = {'author': value['author'],
                             'message': value['message']}
        return branches
