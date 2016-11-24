# MQTT Integration Pack

This pack allows integration with MQTT Brokers

## Configuration

Copy the example configuration in [mqtt.yaml.example](./mqtt.yaml.example)
to `/opt/stackstorm/configs/mqtt.yaml` and edit as required.

* `hostname` - MQTT Broker to connect to
* `subscribe` - An array of MQTT topics to subscribe to (sensor only)
* `port` - MQTT port to connect to (default: 1883)
* `protocol` - MQTT protocol version (default: MQTTv311)
* `client_id` - Client ID to register on MQTT broker
* `userdata` - Custom userdata to include with each MQTT message payload
* `username` - Username to connect to MQTT Broker
* `password` - Password to connect to MQTT Broker
* `ssl` - Enable SSL support (default: false)
* `ssl_cacert` - Path to SSL CA Certificate
* `ssl_cert` - Path to SSL Certificate
* `ssl_key` - Path to SSL Key

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Actions

* `mqtt.publish` - Publish a message onto a MQTT topic

## Sensor

Connects to a MQTT broker, subscribing to various topics and emitting triggers
into the system.

Requires: config setting `subscribe`.
Emits:
  * trigger: mqtt.message
  * payload: topic, message, userdata, qos, retain
