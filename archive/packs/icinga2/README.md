# Icinga2 Integration Pack for Stackstorm

## Description

Icinga2 version 2.4.0 introduced an API, making it possible to subscribe to Icinga2. So far only `StateChange` event type is supported.
Read http://docs.icinga.org/icinga2/latest/doc/module/icinga2/toc#!/icinga2/latest/doc/module/icinga2/chapter/icinga2-api#icinga2-api for more information on Icinga2 API. 

## Configuration

Copy the example configuration in [icinga2.yaml.example](./icinga2.yaml.example)
to `/opt/stackstorm/configs/icinga2.yaml` and edit as required.

* `api_url` - URL to the API stream, e.g. `https://localhost:5665/v1`
* `api_state_change_user` - API user name created on the Icinga2 host, which you are going to connect to, e.g. `root`
* `api_state_change_password` - password for the user name mentioned above
* `api_user` - API user name to query Icinga2 host for objects
* `api_password` - password for the API user

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Actions

* `get_status` - retrieves status from Icinga2 host
* `get_host` - retrieves host objects from Icinga2 host, a list of `hosts` can be provided to narrow down the result
* `get_service` - retrieves service objects from Icinga2 host, a list of `services` can be provided to narrow down the result

## Sensor payload

As of now, sensor is configured to catch only `StateChange` events from Icinga2 host. Typical event of such would consist of:

```
{
  "check_result": {
    "active": true,
    "check_source": "hostname01",
    "command": [
      "/usr/lib64/nagios/plugins/check_disk",
      "-c",
      "10%",
      "-w",
      "20%",
      "-K",
      "10%",
      "-W",
      "20%",
      "-X",
      "none",
      "-X",
      "tmpfs",
      "-X",
      "sysfs",
      "-X",
      "proc",
      "-X",
      "devtmpfs",
      "-X",
      "devfs",
      "-X",
      "mtmfs",
      "-m"
    ],
    "execution_end": 1458668863.9526860714,
    "execution_start": 1458668863.9508030415,
    "exit_status": 0.0,
    "output": "DISK OK - free space: / 3064 MB (54% inode=84%); /boot 78 MB (42% inode=99%); /home 1845 MB (99% inode=99%); /opt 18002 MB (99% inode=99%); /tmp 1846 MB (99% inode=99%); /var 3417 MB (89% inode=98%); /var/log 2089 MB (56% inode=99%);",
    "performance_data": [
      "/=2547MB;4735;5327;0;5919",
      "/boot=105MB;154;173;0;193",
      "/home=3MB;1560;1755;0;1951",
      "/opt=111MB;15268;17177;0;19086",
      "/tmp=3MB;1560;1755;0;1951",
      "/var=409MB;3224;3627;0;4031",
      "/var/log=1609MB;3122;3512;0;3903"
    ],
    "schedule_end": 1458668863.9528689384,
    "schedule_start": 1458668863.9528689384,
    "state": 0.0,
    "type": "CheckResult",
    "vars_after": {
      "attempt": 1.0,
      "reachable": true,
      "state": 0.0,
      "state_type": 0.0
    },
    "vars_before": {
      "attempt": 2.0,
      "reachable": true,
      "state": 1.0,
      "state_type": 0.0
    }
  },
  "host": "hostname01",
  "service": "disk",
  "state": 0.0,
  "state_type": 0.0,
  "timestamp": 1458668870.328537941,
  "type": "StateChange"
}
```

Currently, sensor takes the `host`, `service`, `state`, `state_type`, `type` and `check_result` variables and passes it as a payload to the trigger. All that data can be used in the rule and passed to actions as well.

## TODO

* Re-write actions & sensors to use requests instead of pycurl
