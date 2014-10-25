import boto.ec2
import logging

LOG = logging.getLogger(__name__)


class EC2Client(object):
    def __init__(self, region=None, access_key_id=None, secret_access_key=None):
        self._region = region
        self._access_key_id = access_key_id
        self._secret_access_key = secret_access_key
        self._conn = None

    def connect(self):
        try:
            self._conn = boto.ec2.connect_to_region(self._region,
                                                    aws_access_key_id=self._access_key_id,
                                                    aws_secret_access_key=self._secret_access_key)
        except:
            LOG.exception('Exception connecting to EC2 region: %s', self._region)

    def get_instance_details(self):
        payload = {}
        try:
            instances = self._conn.get_only_instances()
            for i in instances:
                instance_payload = {}
                instance_payload['instance_type'] = i.instance_type
                instance_payload['launch_time'] = i.launch_time
                instance_payload['tags'] = i.tags
                instance_payload['image_id'] = i.image_id
                instance_payload['ip_address'] = i.ip_address
                instance_payload['state'] = i.state
                instance_payload['state_code'] = i.state_code
                payload[i.id] = instance_payload
        except Exception:
            LOG.exception("Failed to get instances.")
        return payload

    def get_volume_details(self):
        payload = {}
        try:
            volumes = self._conn.get_all_volumes()
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
                payload[v.id] = v_payload
        except Exception:
            LOG.exception("Failed to get volumes.")
        return payload
