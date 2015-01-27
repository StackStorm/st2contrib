# Java JMX Integration Pack

This pack allows you to monitor different attributes / metrics exposed by a
Java application through JMX protocol.

This allows you to monitor applications such as Cassandra, Tomacat, Hadoop and
many others.

## Configuration

* ``hostname`` - JMX service hostname.
* ``port`` - JMX service port.
* ``username`` - Optional JMX username.
* ``password`` - Optional JMX password.
* ``object_name`` - Name of the object to be checked.
* ``attribute_name`` - Attribute of the object to be checked.
* ``attribute_keys`` - A list of attribute keys for compound attributes

## Requirements (for running)

* Java JRE >= 1.5

## Requirements (for compiling JMX Query)

* Java JDK 1.5

## Sensors

### JMXSensor

This sensors periodically polls a Java service using JMX protocol for
attributes / metrics specified in the config.

#### jmx.metric trigger

```json
{
    "object_name": "java.lang:type=Memory",
    "attribute_name": "HeapMemoryUsage",
    "attribute_keys": null,
    "metric": {
        "type": "int",
        "name": "used",
        "value": "61385088"
    }
}
```

## Notice

extern/jmxquery/ is part of the [ck-agent project](https://github.com/cloudkick/ck-agent/)
licensed under Apache 2.0 license.
