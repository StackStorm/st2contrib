# Device42 Integration Pack

Integration pack that provides support for Device42, a self-documenting CMDB and single source of truth for all things
IT infrastructure

## Configuration

Copy the example configuration in [device42.yaml.example](./device42.yaml.example)
to `/opt/stackstorm/configs/device42.yaml` and edit as required.

* `d42_server` - Device42 instance address (with protocol and without trailing slash)
* `d42_username` - Device42 username
* `d42_password` - Device42 password
* `verify_certificate` - Set to `false` in case of self-signed SSL certificate

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Supported Actions
```
+-------------------------------+----------+--------------------+---------------------------------------------+
| ref                           | pack     | name               | description                                 |
+-------------------------------+----------+--------------------+---------------------------------------------+
| device42.device_name_list     | device42 | device_name_list   | Returns list of devices names               |
| device42.suggest_next_ip      | device42 | suggest_next_ip    | Suggest next available IP Address           |
| device42.get_dns_zone         | device42 | get_dns_zone       | Returns DNS zone file content for a domain  |
+-------------------------------+----------+--------------------+---------------------------------------------+
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

#### Get `device42.get_dns_zone` for domain
```sh
# st2 run device42.get_dns_zone domain=domain.com

id: 581c7c441d41c804d9067e59
status: succeeded
parameters:
  domain: domain.com
result:
  exit_code: 0
  result: ''@ 3600 IN SOA nh-win2k8r2-vm-03 hostmaster. 107493 900 600 86400 3600       
    @ 600 IN A 192.168.11.161       
    @ 3600 IN NS nh-win2k8r2-vm-03            
    gc._msdcs 600 IN A 192.168.11.161                  
    _ldap._tcp.gc._msdcs 600 IN SRV 0 100 3268 nh-win2k8r2-vm-03'
  stderr: ''
  stdout: ''
```
