import json
import pickle

import pika
from pika.credentials import PlainCredentials

from st2reactor.sensor.base import PollingSensor

DESERIALIZATION_FUNCTIONS = {
    'json': json.loads,
    'pickle': pickle.loads
}


class RabbitMQSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=5):
        super(RabbitMQSensor, self).__init__(sensor_service=sensor_service, config=config,
                                             poll_interval=poll_interval)

    def cleanup(self):
        if self.conn:
            self.conn.close()

    def setup(self):
        self.queues = None
        self.conn = None
        self.channel = None

        self.username = self._config['sensor_config']['username']
        self.password = self._config['sensor_config']['password']
        self.queues = self._config['sensor_config']['queues']
        self.host = self._config['sensor_config']['host']
        self.deserialization_method = self._config['sensor_config']['deserialization_method']

        supported_methods = DESERIALIZATION_FUNCTIONS.keys()
        if self.deserialization_method and self.deserialization_method not in supported_methods:
            raise ValueError('Invalid deserialization method specified: %s' %
                             (self.deserialization_method))

        if self.username and self.password:
            credentials = PlainCredentials(username=self.username, password=self.password)
            connection_params = pika.ConnectionParameters(host=self.host, credentials=credentials)
        else:
            connection_params = pika.ConnectionParameters(host=self.host)

        self.conn = pika.BlockingConnection(connection_params)
        self.channel = self.conn.channel()
        self.channel.basic_qos(prefetch_count=1)

    def poll(self):
        for queue in self.queues:
            queue_state = self.channel.queue_declare(queue=queue, durable=True)
            if queue_state.method.message_count != 0:
                method, properties, body = self.channel.basic_get(queue, no_ack=False)
                self.callback(self.channel, method, properties, body, queue)

    def callback(self, ch, method, properties, body, queue):
        body = self._deserialize_body(body=body)
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
