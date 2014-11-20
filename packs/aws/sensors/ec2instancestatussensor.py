import time

from st2reactor.sensor.base import PollingSensor

from lib.sensorbase import EC2ConnectMixin


class EC2InstanceStatusSensor(PollingSensor, EC2ConnectMixin):
    def __init__(self, sensor_service, config=None, poll_interval=20):
        PollingSensor.__init__(self, sensor_service=sensor_service, config=config,
                               poll_interval=poll_interval)
        EC2ConnectMixin.__init__(self, config=config)

        self._trigger_name = 'instance_status'
        self._trigger_pack = 'aws'
        self._trigger_ref = '.'.join([self._trigger_pack, self._trigger_name])

    def poll(self):
        data = self._ec2.get_instance_details()
        for i in data:
            trigger = self._trigger_ref
            payload = data[i]
            payload['event_id'] = 'ec2-instance-check-' + str(int(time.time()))
            payload['instance_id'] = i
            try:
                self._sensor_service.dispatch(trigger, payload)
            except Exception as e:
                self._log.exception('Exception %s handling st2.ec2.instance_status', e)
