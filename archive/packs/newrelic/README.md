# New Relic Integration Pack

This integration pack allows you to integrate with
[New Relic](http://newrelic.com/).

## Configuration

Copy the example configuration in [newrelic.yaml.example](./newrelic.yaml.example)
to `/opt/stackstorm/configs/newrelic.yaml` and edit as required.

It must contain:

* ``api_url`` - New Relic API URL
* ``api_key`` - New Relic API key
* ``host`` - IP Address sensor should listen on. Default 0.0.0.0
* ``port`` - Port sensor should listen on. Default 10001
* ``url`` - URI path for sensor. Default /st2/nrhook
* ``normal_report_delay`` - Delay before firing return to normal event. Default 300s

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Sensors

New Relic integration pack comes with a sensor which watches for alerts which
are sent via Webhooks from the New Relic API.

Right now it includes two sensors - one for the legacy alerting and API (
``new_relic_legacy_app_sensor.yaml``) and one for the new alerting and API (
``new_relic_app_sensor.yaml``).

By default the legacy sensor is disabled. If you are still using the legacy API
and you want to use the legacy sensor, you should enable it in 
``new_relic_legacy_app_sensor.yaml`` file and disable the new one in
``new_relic_app_sensor.yaml`` file.
