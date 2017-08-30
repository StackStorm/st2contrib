# Libcloud Integration Pack

This integration pack allows you to integrate with
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
* Enable CDN for a container and retrieve container CDN URL -
  `enable_cdn_for_container`
* Retrieve CDN URL of a CDN enabled container - `get_container_cdn_url`
* Retrieve CDN URL for an object which is stored in a CDN enabled container -
  `get_object_cdn_url`

### DNS

* Create a new DNS record - `create_dns_record`
* Delete an existing DNS record - `delete_dns_record`
