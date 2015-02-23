# RabbitMQ Integration Pack

Pack which allows integration with [RabbitMQ](http://www.rabbitmq.com/).

## Actions

* ``list_exchanges`` - List available exchanges.
* ``list_queues`` - List available queues.

Note: All of the actions invoke ``rabbitmqadmin`` tool and must run on the
same node where RabbitMQ server is running (they connect to the local 
instance).
