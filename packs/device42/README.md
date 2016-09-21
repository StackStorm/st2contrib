# Device42 Integration Pack

Integration pack that provides support for Device42, a self-documenting CMDB and  single source of truth for all things
IT infrastructure

## Configuration

* `d42_server` - Device42 instance address (without protocol and trailing slash)
* `d42_username` - Device42 username
* `d42_password` - Device42 password

## Supported Actions
```
+-------------------------------+----------+--------------------+-------------------------------------+
| ref                           | pack     | name               | description                         |
+-------------------------------+----------+--------------------+-------------------------------------+
| device42.device_name_list     | device42 | device_name_list   | Returns list of devices names       |
| device42.suggest_next_ip      | device42 | suggest_next_ip    | Suggest next available IP Address   |
+-------------------------------+----------+--------------------+-------------------------------------+
```

## Examples

#### Get `device42.device_name_list` for FreeBSD
```sh
# st2 run device42.device_name_list os=freebsd

id: 57e2dad51d41c80479ff1de6
status: succeeded
parameters:
  os: freebsd
result:
  exit_code: 0
  result:
  - freebsd
  - freebsd-93-001
  - Unknown
  stderr: ''
  stdout: ''
```

#### Get `device42.suggest_next_ip` for subnet
```sh
# st2 run device42.suggest_next_ip subnet=10.15.24.0/22

id: 57e2d9741d41c80479ff1dc8
status: succeeded
parameters:
  subnet: 10.15.24.0/22
result:
  exit_code: 0
  result: 10.15.24.1
  stderr: ''
  stdout: ''
```