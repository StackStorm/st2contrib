# Java JMX Integration Pack

This pack allows you to monitor different attributes / metrics exposed by a
Java application through JMX protocol.

This allows you to monitor applications such as Cassandra, Tomacat, Hadoop and
many others.

## Configuration

Copy the example configuration in [jmx.yaml.example](./jmx.yaml.example)
to `/opt/stackstorm/configs/jmx.yaml` and edit as required.

* ``hostname`` - JMX service hostname.
* ``port`` - JMX service port.
* ``username`` - Optional JMX username.
* ``password`` - Optional JMX password.
* ``object_name`` - Name of the object to be checked.
* ``attribute_name`` - Attribute of the object to be checked.
* ``attribute_keys`` - A list of attribute keys for compound attributes

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Requirements (for running)

* Java JRE >= 1.5

## Requirements (for compiling JMX Query)

* Java JDK 1.5

## Sensors

### JMXSensor

This sensors periodically polls a Java service using JMX protocol for
attributes / metrics specified in the config.

#### jmx.metric trigger

Example trigger payload:

```json
{
    "jmx_hostname": "localhost",
    "jmx_port": 7199,
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

Note: Each trigger contains only one metric which means that multiple metrics
result in multiple triggers being emitted (one per metric).

## Notice

* ``extern/jmxquery/`` is part of the [ck-agent project](https://github.com/cloudkick/ck-agent/)
licensed under Apache 2.0 license.
* ``extern/cmdline-jmxclient`` is part of the [cmdline-jmxclient](http://crawler.archive.org/cmdline-jmxclient/) project.

## Actions

* ``invoke_method`` -  invokes an arbitrary MBean method which is exposed over
  JMX.
