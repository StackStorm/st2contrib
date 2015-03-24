from st2reactor.sensor.base import PollingSensor
import pika
from pika.credentials import PlainCredentials


class RabbitMQSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=5):
        super(RabbitMQSensor, self).__init__(sensor_service=sensor_service, config=config, poll_interval=poll_interval)

    def cleanup(self):
        if self.conn:
            self.conn.close()

    def setup(self):
        self.queues = None
        self.conn = None
        self.channel = None
        self.user = self._config['sensor_config']['user']
        self.password = self._config['sensor_config']['password']
        self.queues = self._config['sensor_config']['queues']
        host = self._config['sensor_config']['host']
        creds = PlainCredentials(username=self.user, password=self.password)
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=creds))
        self.channel = self.conn.channel()
        self.channel.basic_qos(prefetch_count=1)

    def poll(self):
        for queue in self.queues:
            queue_state = self.channel.queue_declare(queue=queue, durable=True)
            if queue_state.method.message_count != 0:
                method, properties, body = self.channel.basic_get(queue, no_ack=False)
                self.callback(self.channel, method, properties, body, queue)

    def callback(self, ch, method, properties, body, queue):
        payload = {"queue": queue, "body": body}
        self._sensor_service.dispatch(trigger="rabbitmq.new_message", payload=payload)
        self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def update_trigger(self, trigger):
        pass

    def add_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass