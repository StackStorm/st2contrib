# Dimension Data Cloud integration Pack

## Configuration

`config.yaml` requires 2 values, the API username and password. Each action has the region as a parameter, set by default to dd-na (North America)

```yaml
---
api_user: "myusername"
api_password: "mypassword"
```

## Actions

### Compute (VM) actions 

* `add_storage_to_vm`
* `clone_vm_to_image`
* `create_vm_mcp1`
* `create_vm_mcp2`
* `destroy_nic`
* `destroy_vm`
* `disable_monitoring`
* `enable_monitoring`
* `get_vm`
* `get_vm_by_name`
* `get_ipv6_address_of_vm`
* `list_vms`
* `power_off_vm`
* `reboot_vm`
* `reconfigure_vm`
* `remove_storage_from_vm`
* `reset_vm`
* `shutdown_vm`
* `start_vm`
* `update_disk_size`
* `update_disk_speed`
* `update_monitoring_plan`
* `update_vm`
* `update_vm_tools`
* `wait_for_server_operation`

### Network VLAN actions

* `attach_node_to_vlan`
* `create_vlan`
* `delete_vlan`
* `get_vlan`
* `get_vlan_by_name`
* `list_vlans`

### Load Balancer VIP actions for MCP 2.0

* `create_balancer`
* `balancer_attach_member`
* `balancer_delete_node`
* `balancer_detach_member`
* `balancer_list_members`
* `get_balancer`
* `get_balancer_by_name`
* `list_balancers`
* `list_balancer_nodes`
* `list_default_health_monitors`
* `list_pool_members`

### Network 2.0 Network Domain actions

* `create_firewall_rule`
* `create_nat_rule`
* `create_network_domain`
* `create_public_ip_block`
* `delete_network_domain`
* `list_firewall_rules`
* `list_nat_rules`
* `list_network_domains`
* `list_public_ip_blocks`
* `get_network_domain`
* `get_network_domain_by_name`
* `get_public_ip_block`

### General actions

* `configure`
* `get_location_by_id`
* `list_locations`

### Network 1.0 actions

* `create_network`
* `delete_network`
* `list_networks`
* `get_network_by_name`

### Image actions

* `get_image`
* `get_image_by_name`
* `list_customer_images`
* `list_images`
