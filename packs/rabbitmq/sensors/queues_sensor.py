import json
import pickle

import eventlet
import pika

from pika.credentials import PlainCredentials

from st2reactor.sensor.base import Sensor

DESERIALIZATION_FUNCTIONS = {
    'json': json.loads,
    'pickle': pickle.loads
}


class RabbitMQQueueSensor(Sensor):
    """Sensor which monitors a RabbitMQ queue for new messages

    This is a RabbitMQ Queue sensor i.e. it works on the simplest RabbitMQ
    messaging model as described in https://www.rabbitmq.com/tutorials/tutorial-one-python.html.

    It is capable of simultaneously consuming from multiple queues. Each message is
    dispatched to stackstorm as a `rabbitmq.new_message` TriggerInstance.
    """
    def __init__(self, sensor_service, config=None):
        super(RabbitMQQueueSensor, self).__init__(sensor_service=sensor_service, config=config)

        self._logger = self._sensor_service.get_logger(name=self.__class__.__name__)
        self.host = self._config['sensor_config']['host']
        self.username = self._config['sensor_config']['username']
        self.password = self._config['sensor_config']['password']

        queue_sensor_config = self._config['sensor_config']['rabbitmq_queue_sensor']
        self.queues = queue_sensor_config['queues']
        if not isinstance(self.queues, list):
            self.queues = [self.queues]
        self.deserialization_method = queue_sensor_config['deserialization_method']

        supported_methods = DESERIALIZATION_FUNCTIONS.keys()
        if self.deserialization_method and self.deserialization_method not in supported_methods:
            raise ValueError('Invalid deserialization method specified: %s' %
                             (self.deserialization_method))

        self.conn = None
        self.channel = None

    def run(self):
        self._logger.info('Starting to consume messages from RabbitMQ for %s', self.queues)
        # run in an eventlet in-order to yield correctly
        gt = eventlet.spawn(self.channel.start_consuming)
        # wait else the sensor will quit
        gt.wait()

    def cleanup(self):
        if self.conn:
            self.conn.close()

    def setup(self):
        if self.username and self.password:
            credentials = PlainCredentials(username=self.username, password=self.password)
            connection_params = pika.ConnectionParameters(host=self.host, credentials=credentials)
        else:
            connection_params = pika.ConnectionParameters(host=self.host)

        self.conn = pika.BlockingConnection(connection_params)
        self.channel = self.conn.channel()
        self.channel.basic_qos(prefetch_count=1)

        # Setup Qs for listening
        for queue in self.queues:
            self.channel.queue_declare(queue=queue, durable=True)

            def callback(ch, method, properties, body):
                self._dispatch_trigger(ch, method, properties, body, queue)

            self.channel.basic_consume(callback, queue=queue)

    def _dispatch_trigger(self, ch, method, properties, body, queue):
        body = self._deserialize_body(body=body)
        self._logger.debug('Received message for queue %s with body %s', queue, body)

        payload = {"queue": queue, "body": body}
        try:
            self._sensor_service.dispatch(trigger="rabbitmq.new_message", payload=payload)
        finally:
            self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def update_trigger(self, trigger):
        pass

    def add_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _deserialize_body(self, body):
        if not self.deserialization_method:
            return body

        deserialization_func = DESERIALIZATION_FUNCTIONS[self.deserialization_method]

        try:
            body = deserialization_func(body)
        except Exception:
            pass

        return body
