# FireEye Integration Pack

StackStorm integration with FireEye CM and AX threat intelligence devices

## Configuration

Copy the example configuration in [fireeye.yaml.example](./fireeye.yaml.example)
to `/opt/stackstorm/configs/fireeye.yaml` and edit as required.

* `api_url` - HTTPS endpoint of FireEye CM appliance. (e.g.: https://fqdn.to.device)
* `username` - FireEye username
* `password` - FireEye password

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Actions

* `fireeye.get_alert_query`         - Request existing alert profiles with optional filters
* `fireeye.get_submission_results`  - Query results of completed job
* `fireeye.get_submission_status`   - Query status of running job
* `fireeye.submit_malware`          - Submit a Malware object to FireEye AX appliance
* `fireeye.view_ax_config`          - Returns a list of profiles and applications on AX devices
