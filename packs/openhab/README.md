# OpenHAB Integration Pack

This pack allows you to integrate with [OpenHAB](http://openhab.org).

## Configuration

Copy the example configuration in [openhab.yaml.example](./openhab.yaml.example)
to `/opt/stackstorm/configs/openhab.yaml` and edit as required.

* `hostname` - Hostname of OpenHAB
* `port` - Port OpenHAB listens on (default: 8080)
* `username` - Username to connect to OpenHAB (optional)
* `password` - Password to connect to OpenHAB (optional)

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Actions

* `get_status` - Set the status of an OpenHAB item
* `send_command` - Send a command to an OpenHAB item
* `set_state` - Set the state of an OpenHAB item
