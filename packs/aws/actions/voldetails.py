from lib import action


class VolumeDetails(action.BaseAction):

    def run(self, volume_id):
        return self.ec2.getVolumeDetails(volume_id)
