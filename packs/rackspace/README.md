# Rackspace Integration Pack

Packs which allows integration with [Rackspace
Cloud](http://www.rackspace.com/cloud) services such as:

* Cloud Servers
* Cloud Load Balancers
* Cloud DNS

## Configuration

* ``username`` - Your cloud account username.
* ``api_key`` - Your cloud account API key.
* ``region`` - Default region to use for all the operations. Can be overriden
  on per action basis.
* ``debug`` - True to enable debug mode.

## Actions

### Virtual Machines / Cloud Servers

* `list_vms` - List all the available VMs.
* `create_vm` - Create a new VM.
* `delete_vm` - Delete an existing VM.
* `get_vm_info` - Retrieve details on a single VM
* `list_vm_ips` - Return a list of all managed IPs by metadata/count
* `list_vm_ids` - Return a list of all managed IDs by metadata/count
* `list_vm_names` - Return a list of all managed names by metadata/count

### Cloud Load Balancers

* `create_loadbalancer` - Create a new load balancer.
* `add_node_to_loadbalancer` - Add VM to the load balancer.
* `delete_node_from_loadbalancer` - Remove a VM from the load balancer.

### Cloud DNS

* `list_dns_zones` - List all the DNS zones.
* `list_dns_records` - List all the records for a particular zone.
* `create_dns_zone` - Create a new DNS zone.
* `delete_dns_zone` - Delete an existing zone.
* `create_dns_record` - Create a new DNS record.
* `delete_dns_record` - Delete an existing DNS record.
