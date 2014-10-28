import six
from lib import action


class VolumeDetails(action.BaseAction):

    def run(self, volume_id, delete=False):
        orphaned = {}
        volumes = self.ec2.getVolumeDetails(volume_id)
        for _id, volume in six.iteritems(volumes):
            if 'available' in volume['status']:
                orphaned[_id] = volume
        if delete:
            map(self.ec2.deleteVolume, six.iterkeys(orphaned))
        return orphaned
