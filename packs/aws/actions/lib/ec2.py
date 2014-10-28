import logging
import time
import boto.ec2


LOG = logging.getLogger(__name__)


class EC2(object):

    def __init__(self, config):
        self._region = config['region']
        self._access_key_id = config['access_key_id']
        self._secret_access_key = config['secret_access_key']
        self._interval = config['interval']
        self._conn = self.connect(self._region)

    def connect(self, region):
        return boto.ec2.connect_to_region(region,
                                          aws_access_key_id=self._access_key_id,
                                          aws_secret_access_key=self._secret_access_key)

    def getInstanceDetails(self, instance_id=None, iponly=False):
        LOG.debug('Retrieving deatils for instance %s.', instance_id)
        payload = {}
        instance_ids = [instance_id] if instance_id else None
        instances = self._conn.get_only_instances(instance_ids=instance_ids)
        for i in instances:
            instance_payload = {}
            payload[i.id] = instance_payload
            instance_payload['ip_address'] = i.ip_address
            if iponly:
                continue
            instance_payload['instance_type'] = i.instance_type
            instance_payload['launch_time'] = i.launch_time
            instance_payload['tags'] = i.tags
            instance_payload['image_id'] = i.image_id
            instance_payload['ip_address'] = i.ip_address
            instance_payload['state'] = i.state
            instance_payload['state_code'] = i.state_code
        LOG.debug(payload)
        return payload

    def getVolumeDetails(self, volume_id=None):
        LOG.debug('Retrieving details for volume %s.', volume_id)
        payload = {}
        volume_ids = [volume_id] if volume_id else None
        volumes = self._conn.get_all_volumes(volume_ids=volume_ids)
        for v in volumes:
            v_payload = {}
            v_payload['create_time'] = v.create_time
            v_payload['region'] = v.region.name
            v_payload['size'] = v.size
            v_payload['status'] = v.status
            v_payload['tags'] = v.tags
            v_payload['type'] = v.type
            v_payload['attach_time'] = v.attach_data.attach_time
            v_payload['device_map'] = v.attach_data.device
            v_payload['instance_id'] = v.attach_data.instance_id
        LOG.debug(payload)
        return payload

    def getAMI(self, ami=None, owner=None):
        image_list = {}
        image_ids = [ami] if ami else None
        images = self._conn.get_all_images(image_ids=image_ids, owners=strToList(owner))
        for i in images:
            image_data = {}
            image_data['name'] = i.name
            image_data['state'] = i.state
            image_data['architecture'] = i.architecture
            image_data['root_device_type'] = i.root_device_type
        return image_list

    def deregisterAMI(self, ami):
        output = {}
        image = self._conn.get_all_images(image_ids=strToList(ami))
        result = image[0].deregister()
        output[result] = [ami]
        return output

    def createVM(self, ami, instance_type):
        i = {}
        output = []
        reservation = self._conn.run_instances(
            ami,
            instance_type=instance_type)
        instance = reservation.instances[0]
        time.sleep(2)
        status = instance.update()
        while status == 'pending':
            time.sleep(10)
            status = instance.update()
        if status == 'running':
            i[instance.id] = {}
            i[instance.id]['public_dns'] = instance.public_dns_name
            i[instance.id]['private_dns'] = instance.private_dns_name
            i[instance.id]['status'] = status
            output.append(i)

        return output

    def changeVmState(self, state, instance_id):
        results = []
        result_ids = []
        output = {}
        instances = strToList(instance_id)
        LOG.debug(instances)
        if state == 'start':
            results = self._conn.start_instances(instances)
        elif state == 'stop':
            results = self._conn.stop_instances(instances)
        elif state == 'destroy' or state == 'terminate':
            state = 'terminate'
            results = self._conn.terminate_instances(instances)
        for i in results:
            result_ids.append(i.id)
        output[state] = result_ids
        return output

    def attachNewVolume(self, size, instance_id, dev):
        output = {}
        volume_id = self._conn.create_volume(size, self._region)
        output['status'] = self._conn.attach_volume(
            volume_id,
            instance_id,
            dev)
        return output

    def deleteVolume(self, vol_id):
        output = {}
        results = self._conn.delete_volume(vol_id)
        if results is True:
            status = 'deleted'
        else:
            status = 'failed'
        output[status] = vol_id
        return output

    def attachEIP(self, ip=None):
        raise NotImplementedError('attachEIP not implemented.')

    def createImage(self, instance_id):
        raise NotImplementedError('createImage not implemented.')


def strToList(data):
    new_list = []
    if not isinstance(data, list):
        new_list.append(data)
    else:
        new_list = data
    return new_list
