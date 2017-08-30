import mock
import yaml

from st2tests.base import BaseSensorTestCase

from sqs_sensor import AWSSQSSensor


class MockQueue(object):
    def __init__(self, msgs=[]):
        self.dummy_messages = [MockMessage(x) for x in msgs]

    def receive_messages(self, **kwargs):
        return self.dummy_messages


class MockMessage(object):
    def __init__(self, body=None):
        self.body = body

    def delete(self):
        return mock.MagicMock(return_value=None)


class SQSSensorTestCase(BaseSensorTestCase):
    sensor_cls = AWSSQSSensor

    def setUp(self):
        super(SQSSensorTestCase, self).setUp()

        self.full_config = self.load_yaml('full.yaml')

    def load_yaml(self, filename):
        return yaml.safe_load(self.get_fixture_content(filename))

    def test_poll_without_message(self):
        sensor = self.get_sensor_instance(config=self.full_config)

        sensor.setup()

        # replace ServiceResource object to mock
        sensor.sqs_res = mock.MagicMock()
        sensor.sqs_res.get_queue_by_name = mock.MagicMock(return_value=MockQueue())

        sensor.poll()

        self.assertEqual(self.get_dispatched_triggers(), [])

    def test_poll_with_message(self):
        sensor = self.get_sensor_instance(config=self.full_config)

        sensor.setup()

        # replace ServiceResource object to mock
        sensor.sqs_res = mock.MagicMock()
        sensor.sqs_res.get_queue_by_name = mock.MagicMock(return_value=MockQueue(['foo']))

        sensor.poll()

        self.assertTriggerDispatched(trigger='aws.sqs_new_message')
        self.assertNotEqual(self.get_dispatched_triggers(), [])
