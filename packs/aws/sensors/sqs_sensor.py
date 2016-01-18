"""
This is generic SQS Sensor using boto3 api to fetch messages from sqs queue.
After receiving a messge it's content is passed as payload to a trigger 'aws.sqs_new_message'

This sensor can be configured either by using config.yaml withing a pack or by creating
following values in datastore:
    - aws.input_queue
    - aws.aws_access_key_id
    - aws.aws_secret_access_key
    - aws.region
"""

from boto3.session import Session
from botocore.exceptions import ClientError

from st2reactor.sensor.base import PollingSensor


class AWSSQSSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=5):
        super(AWSSQSSensor, self).__init__(sensor_service=sensor_service, config=config,
                                           poll_interval=poll_interval)

    def setup(self):
        self.input_queue = self._GetConfigEntry(key='input_queue', prefix='sqs_sensor')
        self.aws_access_key = self._GetConfigEntry('aws_access_key_id')
        self.aws_secret_key = self._GetConfigEntry('aws_secret_access_key')
        self.aws_region = self._GetConfigEntry('region')

        self._logger = self._sensor_service.get_logger(name=self.__class__.__name__)

        self.session = None
        self.sqs_res = None

        self._SetupSqs()
        self.queue = self._GetQueueByName(self.input_queue)

    def poll(self):
        msg = self._receive_messages(queue=self.queue)
        if msg:
            payload = {"queue": self.input_queue, "body": msg[0].body}
            self._sensor_service.dispatch(trigger="aws.sqs_new_message", payload=payload)
            msg[0].delete()

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        # This method is called when trigger is created
        pass

    def update_trigger(self, trigger):
        # This method is called when trigger is updated
        pass

    def remove_trigger(self, trigger):
        pass

    def _GetConfigEntry(self, key, prefix='setup'):
        ''' Get configuration values either from Datastore or config file. '''
        config = self._config.get(prefix, None)

        value = self._sensor_service.get_value('aws.%s' % (key), local=False)
        if not value:
            value = config.get(key, None)

        return value

    def _SetupSqs(self):
        ''' Setup Boto3 structures '''
        self._logger.debug('Setting up SQS resources')
        self.session = Session(aws_access_key_id=self.aws_access_key,
                               aws_secret_access_key=self.aws_secret_key,
                               region_name=self.aws_region)

        self.sqs_res = self.session.resource('sqs')

    def _GetQueueByName(self, queueName):
        ''' Fetch QUEUE by it's name create new one if queue doesn't exist '''
        try:
            queue = self.sqs_res.get_queue_by_name(QueueName=queueName)
        except ClientError as e:
            self._logger.warning("SQS Queue: %s doesn't exist, creating it.", queueName)
            if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
                queue = self.sqs_res.create_queue(QueueName=queueName)
            else:
                raise

        return queue

    def _receive_messages(self, queue, wait_time=2, num_messages=1):
        ''' Receive a message from queue and return it. '''
        msg = queue.receive_messages(WaitTimeSeconds=wait_time, MaxNumberOfMessages=num_messages)

        return msg
