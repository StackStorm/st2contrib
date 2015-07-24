# FireEye Integration Pack

StackStorm integration with FireEye CM and AX threat intelligence devices

## Configuration

* `api_url` - HTTPS endpoint of FireEye CM appliance. (e.x.: https://fqdn.to.device)
* `username` - FireEye username
* `password` - FireEye password

## Actions

* `fireeye.get_alert_query`         - Request existing alert profiles with optional filters
* `fireeye.get_submission_results`  - Query results of completed job
* `fireeye.get_submission_status`   - Query status of running job
* `fireeye.submit_malware`          - Submit a Malware object to FireEye AX appliance
* `fireeye.view_ax_config`          - Returns a list of profiles and applications on AX devices
