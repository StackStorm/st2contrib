import unittest2
import mock

from st2tests.mocks.sensor import MockSensorService

from docker_container_sensor import DockerSensor

MOCK_CONTAINER_DATA = {
    "Id": "8dfafdbc3a40",
    "Names": ["/boring_feynman"],
    "Image": "ubuntu:latest",
    "Command": "echo 1",
    "Created": 1367854155,
    "Status": "Exit 0",
    "Ports": [{"PrivatePort": 2222, "PublicPort": 3333, "Type": "tcp"}],
    "SizeRw": 12288,
    "SizeRootFs": 0
}


class DockerSensorTestCase(unittest2.TestCase):
    def test_poll(self):
        # TODO: Move to base test class
        sensor_service = MockSensorService(sensor_wrapper=None)
        sensor = DockerSensor(sensor_service=sensor_service)

        # No existing and no running containers (e.g. after initial sensor poll)
        sensor._running_containers = {}
        sensor._get_active_containers = mock.Mock()
        sensor._get_active_containers.return_value = {}

        sensor.poll()
        self.assertEqual(sensor_service._dispatched_triggers, [])

        # One new container
        sensor._get_active_containers.return_value = {'1': MOCK_CONTAINER_DATA}

        sensor.poll()
        self.assertEqual(len(sensor_service._dispatched_triggers), 1)
        sensor_service.assertTriggerDispatched(trigger='docker.container_tracker.started',
                                               payload={'container_info': MOCK_CONTAINER_DATA})

        # One container stopped
        sensor._get_active_containers.return_value = {}
        sensor.poll()
        self.assertEqual(len(sensor_service._dispatched_triggers), 2)
        sensor_service.assertTriggerDispatched(trigger='docker.container_tracker.stopped',
                                               payload={'container_info': MOCK_CONTAINER_DATA})
