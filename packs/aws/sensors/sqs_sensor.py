"""
This is generic SQS Sensor using boto3 api to fetch messages from sqs queue.
After receiving a message it's content is passed as payload to a trigger 'aws.sqs_new_message'

This sensor can be configured either by using config.yaml withing a pack or by creating
following values in datastore:
    - aws.input_queues (list queues as comma separrated string: first_queue,second_queue)
    - aws.aws_access_key_id
    - aws.aws_secret_access_key
    - aws.region

For configuration in config.yaml with config like this
    setup:
      aws_access_key_id:
      aws_access_key_id:
      region:
    sqs_sensor:
      input_queues:
        - first_queue
        - second_queue

If any value exist in datastore it will be taken instead of any value in config.yaml
"""

from boto3.session import Session
from botocore.exceptions import ClientError

from st2reactor.sensor.base import PollingSensor


class AWSSQSSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=5):
        super(AWSSQSSensor, self).__init__(sensor_service=sensor_service, config=config,
                                           poll_interval=poll_interval)

    def setup(self):
        queues = self._get_config_entry(key='input_queues', prefix='sqs_sensor')

        # XXX: This is a hack as from datastore we can only receive a string while
        # from config.yaml we can receive a list
        if type(queues) is str:
            self.input_queues = queues.split(', ')
        else:
            self.input_queues = queues

        self.aws_access_key = self._get_config_entry('aws_access_key_id')
        self.aws_secret_key = self._get_config_entry('aws_secret_access_key')
        self.aws_region = self._get_config_entry('region')

        self._logger = self._sensor_service.get_logger(name=self.__class__.__name__)

        self.session = None
        self.sqs_res = None

        self._setup_sqs()

    def poll(self):
        for queue in self.input_queues:
            msg = self._receive_messages(queue=self._get_queue_by_name(queue))
            if msg:
                payload = {"queue": queue, "body": msg[0].body}
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

    def _get_config_entry(self, key, prefix='setup'):
        ''' Get configuration values either from Datastore or config file. '''
        config = self._config.get(prefix, None)

        value = self._sensor_service.get_value('aws.%s' % (key), local=False)
        if not value:
            value = config.get(key, None)

        if not value:
            raise ValueError('[AWSSQSSensor]: Configuration for %s key is missing.' % (key))

        return value

    def _setup_sqs(self):
        ''' Setup Boto3 structures '''
        self._logger.debug('Setting up SQS resources')
        self.session = Session(aws_access_key_id=self.aws_access_key,
                               aws_secret_access_key=self.aws_secret_key,
                               region_name=self.aws_region)

        self.sqs_res = self.session.resource('sqs')

    def _get_queue_by_name(self, queueName):
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
