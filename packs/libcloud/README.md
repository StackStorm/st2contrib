# Libcloud Content Pack

This content pack allows you to integrate with
[Apache Libcloud](http://libcloud.apache.org/).

## Actions

Currently, the following actions listed bellow are supported:

### Virtual Machines / Servers

* Create a new VM - `create_vm`
* Reboot a VM - `reboot_vm`
* Stop a VM - `stop_vm`
* Start a VM - `start_vm`
* Destroy a VM - `destroy_vm`

### Storage

* Upload a file to a container - `upload_file`
* Enable CDN for a container and retrieve container CDN URL
  - `enable_cdn_for_container`

### DNS

* Create a new DNS record - `create_dns_record`
* Delete an existing DNS record - `delete_dns_record`
