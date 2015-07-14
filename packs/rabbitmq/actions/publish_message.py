import pika

from st2actions.runners.pythonrunner import Action


class PublishMessageAction(Action):
    def run(self, host, port, username, password, virtual_host, exchange, exchange_type,
            exchange_durable, routing_key, message):
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(host, port, virtual_host, credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange, type=exchange_type, durable=exchange_durable)
        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
        connection.close()
