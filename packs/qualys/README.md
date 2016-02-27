# Qualys Security integration pack

Read [API Documentation](https://www.qualys.com/docs/qualys-api-v2-user-guide.pdf) for vendor details.

## Configuration

`config.yaml` requires 3 properties:
* `hostname` The host of the Qualys API serivce
* `username` User to the API
* `password` Password to the API

```yaml
---
hostname: qualysapi.serviceprovider.com
username: jerry
password: I<3Elaine
```

## Actions

* `add_host` Add host to vulnerability management, policy compliance, or both.
* `get_host` Get the status of a host, e.g. last scanned, NETBIOS details
* `get_host_range` Get the status of an IP range of hosts
* `launch_scan` Launch a scan on a host
* `list_scans` List scans