import re
import six
from lib import action


class DeregisterAMI(action.BaseAction):

    def run(self, search, pattern):
        ami_ids = self._find_amis(self.ec2, search, pattern)
        return self._deregister_amis(self.ec2, ami_ids)

    @staticmethod
    def _find_amis(client, search, pattern):
        amis = client.getAMI(owner="self")
        matched_ami_ids = []
        for ami_id, ami in six.iteritems(amis):
            if search == 'id':
                if re.search(pattern, ami_id):
                    matched_ami_ids.append(ami_id)
            elif search == 'name':
                if re.search(pattern, ami['name']):
                    matched_ami_ids.append(ami_id)
        return matched_ami_ids

    @staticmethod
    def _deregister_amis(client, ami_ids):
        result = {}
        for ami_id in ami_ids:
            out = client.deregisterAMI(ami_id)
            result[ami_id] = out
        return result
