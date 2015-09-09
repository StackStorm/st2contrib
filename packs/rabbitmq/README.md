# RabbitMQ Integration Pack

Pack which allows integration with [RabbitMQ](http://www.rabbitmq.com/).

## Actions

* ``list_exchanges`` - List available exchanges.
* ``list_queues`` - List available queues.
* ``publish_message`` - Publish a message to a RabbitMQ service.

Note: ``list_exchanges`` and ``list_queues`` invoke ``rabbitmqadmin`` tool and must run on the
same node where RabbitMQ server is running (they connect to the local instance).

### publish_message example

The following action will publish a message to a remote RabbitMQ server with a stunnel-based tunnel preconfigured:

```shell
$ st2 run rabbitmq.publish_message host=localhost port=5673 virtual_host=sensu exchange=metrics exchange_type=topic username=sensu password=password message="foo.bar.baz 1 1436802746"
```


## Sensors

* ``new_message`` - Sensor that triggers a rabbitmq.new_message with a payload containing the queue and the body

This sensor should only be used with ``fanout`` and ``topic`` exchanges,  this way it doesn't affect the behavior of the app since messages will still be delivered to other consumers / subscribers.
If it's used with ``direct`` or ``headers`` exchanges, those messages won't be delivered to other consumers so it will affect app behavior and potentially break it.

## Sensors Config

* ``host`` - RabbitMQ host to connect to.
* ``username`` - Username to connect to RabbitMQ (optional).
* ``password`` - Password to connect to RabbitMQ (optional).
* ``queues`` - List of queues to check for messages. See an example below.
* ``deserialization_method`` - Which method to use to de-serialize the
  message body. By default, no deserialization method is specified which means
  the message body is left as it is. Valid values are ``json`` and ``pickle``.

```yaml
sensor_config:
  queues:
    - queue1
    - queue2
    - ....
```
