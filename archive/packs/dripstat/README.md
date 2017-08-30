# Dripstat Integration Pack

Pack which allows integration with [Dripstat](https://dripstat.com).

## Configuration

Copy the example configuration in [dripstat.yaml.example](./dripstat.yaml.example)
to `/opt/stackstorm/configs/dripstat.yaml` and edit as required.

* ``api_key`` - Service API Key

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Sensors

### DripstatAlertSensor

This sensor monitors all configured applications and dispatches a trigger

Currently supported event types:

* ``AlertEvent`` - Triggered when an alert is detected for an application.

#### dripstat.alert trigger

Example trigger payload:

```json
{
    "app_name": "Chronon",
    "alert_name": "heap",
    "started_at": "1422287520",
    "jvm_host": "host001"
}
```
