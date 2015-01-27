# Dripstat Integration Pack

Pack which allows integration with [Dripstat](https://dripstat.com).

## Configuration

* ``api_key`` - Service API Key

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
