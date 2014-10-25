import time

from lib.sensorbase import EC2ConnectMixin


class EC2VolumeStatusSensor(EC2ConnectMixin):
    def __init__(self, container_service, config=None):
        super(EC2VolumeStatusSensor, self).__init__(config)
        self._container_service = container_service
        self._interval = config.get('interval', 20)

    def start(self):
        while True:
            data = self.ec2.get_volume_details()
            for i in data:
                trigger = {}
                trigger['name'] = 'st2.ec2.volume_status'

                payload = data[i]
                payload['event_id'] = 'ec2-volume-status-check-' + str(int(time.time()))
                payload['volume_id'] = i
                try:
                    self._container_service.dispatch(trigger, payload)
                except Exception as e:
                    self._log.exception('Exception %s handling st2.ec2.instance_status', e)

            time.sleep(self._interval)

    def get_trigger_types(self):
        return [
            {
                'name': 'st2.ec2.volume_status',
                'description': 'EC2 Volume Status Sensor',
                'payload_schema': {
                    'type': 'object',
                    'properties': {
                        'volume_id': {},
                        'create_time': {},
                        'launch_time': {},
                        'region': {},
                        'size': {},
                        'status': {},
                        'tags': {},
                        'type': {},
                        'attach_time': {},
                        'device_map': {},
                        'instance_id': {}
                    }
                }
            }
        ]
