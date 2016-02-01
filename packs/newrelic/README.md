# New Relic Integration Pack

This integration pack allows you to integrate with
[New Relic](http://newrelic.com/).

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
