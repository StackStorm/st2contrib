# StackStorm Community Repo

[![Gitter](https://badges.gitter.im/Join Chat.svg)](https://gitter.im/StackStorm/st2contrib?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![StackStorm](https://github.com/stackstorm/st2/raw/master/stackstorm_logo.png)](http://www.stackstorm.com)

[![Build Status](https://travis-ci.org/StackStorm/st2contrib.svg?branch=master)](https://travis-ci.org/StackStorm/st2contrib)

Contents of this repository are comprise of integrations and automations that
are consumed by the [StackStorm automation platform](http://www.stackstorm.com/product/).

* Get [StackStorm](http://www.stackstorm.com/start-now/).
* Explore community portal at [stackstorm.com/community](http://www.stackstorm.com/community).
* Read the docs to learn how to use integration packs with StackStorm at
  [docs.stackstorm.com](http://docs.stackstorm.com/packs.html).

## Packs

Actions, Sensors and Rules all organized neatly into to domain or tool specific
packs.

## Extra

Related tools that help make it easier to integrate and consume StackStorm content.

## Tests and Automated Checks

To run tests and all the other automated checks which run on Travis CI, run the following
command:

```bash
make all
```

## Available Packs

Name | Description | Author | Latest Version | Available Resources
---- | ----------- | ------ | -------------- | -------------------
| [aws](https://github.com/StackStorm/st2contrib/tree/master/packs/aws) | st2 content pack containing Amazon Web Services integrations. | [st2-dev](mailto:info@stackstorm.com) | 0.2 | [click](https://github.com/StackStorm/st2contrib#aws-pack)
| [docker](https://github.com/StackStorm/st2contrib/tree/master/packs/docker) | st2 content pack containing docker integrations | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#docker-pack)
| [dripstat](https://github.com/StackStorm/st2contrib/tree/master/packs/dripstat) | Integration with the Dripstat Application Performance Monitoring tool | [James Fryman](mailto:james@fryman.io) | 0.0.1 | [click](https://github.com/StackStorm/st2contrib#dripstat-pack)
| [git](https://github.com/StackStorm/st2contrib/tree/master/packs/git) | st2 content pack containing git integrations | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#git-pack)
| [github](https://github.com/StackStorm/st2contrib/tree/master/packs/github) | st2 content pack containing github integrations | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#github-pack)
| [irc](https://github.com/StackStorm/st2contrib/tree/master/packs/irc) | st2 content pack containing irc integrations | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#irc-pack)
| [jira](https://github.com/StackStorm/st2contrib/tree/master/packs/jira) | st2 content pack containing jira integrations | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#jira-pack)
| [jmx](https://github.com/StackStorm/st2contrib/tree/master/packs/jmx) | st2 content pack containing Java JMX integrations | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#jmx-pack)
| [libcloud](https://github.com/StackStorm/st2contrib/tree/master/packs/libcloud) | st2 content pack containing libcloud integrations | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#libcloud-pack)
| [linux](https://github.com/StackStorm/st2contrib/tree/master/packs/linux) | Generic linux actions | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#linux-pack)
| [nagios](https://github.com/StackStorm/st2contrib/tree/master/packs/nagios) | Nagios integration pack. See README.md for setup instructions. | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#nagios-pack)
| [newrelic](https://github.com/StackStorm/st2contrib/tree/master/packs/newrelic) | st2 content pack containing newrelic integrations | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#newrelic-pack)
| [openstack](https://github.com/StackStorm/st2contrib/tree/master/packs/openstack) | st2 content pack containing openstack integrations | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#openstack-pack)
| [puppet](https://github.com/StackStorm/st2contrib/tree/master/packs/puppet) | st2 content pack containing puppet integrations | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#puppet-pack)
| [sensu](https://github.com/StackStorm/st2contrib/tree/master/packs/sensu) | st2 content pack containing sensu integrations | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#sensu-pack)
| [slack](https://github.com/StackStorm/st2contrib/tree/master/packs/slack) | st2 content pack containing slack integrations | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#slack-pack)
| [twilio](https://github.com/StackStorm/st2contrib/tree/master/packs/twilio) | st2 content pack containing twilio integrations | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#twilio-pack)
| [twitter](https://github.com/StackStorm/st2contrib/tree/master/packs/twitter) | st2 content pack containing twitter integrations | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#twitter-pack)
### aws pack

#### Actions

Name | Description
---- | -----------
create_vm | Create a VM, add DNS to Route53
destroy_vm | Destroys a VM and removes it from Route53
ec2_allocate_address | 
ec2_assign_private_ip_addresses | 
ec2_associate_address | 
ec2_associate_address_object | 
ec2_attach_network_interface | 
ec2_attach_volume | 
ec2_authorize_security_group | 
ec2_authorize_security_group_deprecated | 
ec2_authorize_security_group_egress | 
ec2_build_base_http_request | 
ec2_build_complex_list_params | 
ec2_build_configurations_param_list | 
ec2_build_filter_params | 
ec2_build_list_params | 
ec2_build_tag_param_list | 
ec2_bundle_instance | 
ec2_cancel_bundle_task | 
ec2_cancel_reserved_instances_listing | 
ec2_cancel_spot_instance_requests | 
ec2_close | 
ec2_confirm_product_instance | 
ec2_copy_image | 
ec2_copy_snapshot | 
ec2_create_image | 
ec2_create_key_pair | 
ec2_create_network_interface | 
ec2_create_placement_group | 
ec2_create_reserved_instances_listing | 
ec2_create_security_group | 
ec2_create_snapshot | 
ec2_create_spot_datafeed_subscription | 
ec2_create_tags | 
ec2_create_volume | 
ec2_delete_key_pair | 
ec2_delete_network_interface | 
ec2_delete_placement_group | 
ec2_delete_security_group | 
ec2_delete_snapshot | 
ec2_delete_spot_datafeed_subscription | 
ec2_delete_tags | 
ec2_delete_volume | 
ec2_deregister_image | 
ec2_describe_account_attributes | 
ec2_describe_reserved_instances_modifications | 
ec2_describe_vpc_attribute | 
ec2_detach_network_interface | 
ec2_detach_volume | 
ec2_disassociate_address | 
ec2_enable_volume_io | 
ec2_get_all_addresses | 
ec2_get_all_bundle_tasks | 
ec2_get_all_images | 
ec2_get_all_instance_status | 
ec2_get_all_instance_types | 
ec2_get_all_instances | 
ec2_get_all_kernels | 
ec2_get_all_key_pairs | 
ec2_get_all_network_interfaces | 
ec2_get_all_placement_groups | 
ec2_get_all_ramdisks | 
ec2_get_all_regions | 
ec2_get_all_reservations | 
ec2_get_all_reserved_instances | 
ec2_get_all_reserved_instances_offerings | 
ec2_get_all_security_groups | 
ec2_get_all_snapshots | 
ec2_get_all_spot_instance_requests | 
ec2_get_all_tags | 
ec2_get_all_volume_status | 
ec2_get_all_volumes | 
ec2_get_all_zones | 
ec2_get_console_output | 
ec2_get_http_connection | 
ec2_get_image | 
ec2_get_image_attribute | 
ec2_get_instance_attribute | 
ec2_get_key_pair | 
ec2_get_list | 
ec2_get_object | 
ec2_get_only_instances | 
ec2_get_params | 
ec2_get_password_data | 
ec2_get_path | 
ec2_get_proxy_auth_header | 
ec2_get_proxy_url_with_auth | 
ec2_get_snapshot_attribute | 
ec2_get_spot_datafeed_subscription | 
ec2_get_spot_price_history | 
ec2_get_status | 
ec2_get_utf8_value | 
ec2_get_volume_attribute | 
ec2_handle_proxy | 
ec2_import_key_pair | 
ec2_make_request | 
ec2_modify_image_attribute | 
ec2_modify_instance_attribute | 
ec2_modify_network_interface_attribute | 
ec2_modify_reserved_instances | 
ec2_modify_snapshot_attribute | 
ec2_modify_volume_attribute | 
ec2_modify_vpc_attribute | 
ec2_monitor_instance | 
ec2_monitor_instances | 
ec2_new_http_connection | 
ec2_prefix_proxy_to_path | 
ec2_proxy_ssl | 
ec2_purchase_reserved_instance_offering | 
ec2_put_http_connection | 
ec2_reboot_instances | 
ec2_register_image | 
ec2_release_address | 
ec2_request_spot_instances | 
ec2_reset_image_attribute | 
ec2_reset_instance_attribute | 
ec2_reset_snapshot_attribute | 
ec2_revoke_security_group | 
ec2_revoke_security_group_deprecated | 
ec2_revoke_security_group_egress | 
ec2_run_instances | 
ec2_server_name | 
ec2_set_host_header | 
ec2_set_request_hook | 
ec2_skip_proxy | 
ec2_start_instances | 
ec2_stop_instances | 
ec2_terminate_instances | 
ec2_trim_snapshots | 
ec2_unassign_private_ip_addresses | 
ec2_unmonitor_instance | 
ec2_unmonitor_instances | 
ec2_wait_for_state | 
r53_build_base_http_request | 
r53_change_rrsets | 
r53_close | 
r53_create_health_check | 
r53_create_hosted_zone | 
r53_create_zone | 
r53_delete_health_check | 
r53_delete_hosted_zone | 
r53_get_all_hosted_zones | 
r53_get_all_rrsets | 
r53_get_change | 
r53_get_hosted_zone | 
r53_get_hosted_zone_by_name | 
r53_get_http_connection | 
r53_get_list_health_checks | 
r53_get_path | 
r53_get_proxy_auth_header | 
r53_get_proxy_url_with_auth | 
r53_get_zone | 
r53_get_zones | 
r53_handle_proxy | 
r53_make_request | 
r53_new_http_connection | 
r53_prefix_proxy_to_path | 
r53_proxy_ssl | 
r53_put_http_connection | 
r53_server_name | 
r53_set_host_header | 
r53_set_request_hook | 
r53_skip_proxy | 
r53_zone_add_a | 
r53_zone_add_cname | 
r53_zone_add_mx | 
r53_zone_add_record | 
r53_zone_delete | 
r53_zone_delete_a | 
r53_zone_delete_cname | 
r53_zone_delete_mx | 
r53_zone_delete_record | 
r53_zone_find_records | 
r53_zone_get_a | 
r53_zone_get_cname | 
r53_zone_get_mx | 
r53_zone_get_nameservers | 
r53_zone_get_records | 
r53_zone_update_a | 
r53_zone_update_cname | 
r53_zone_update_mx | 
r53_zone_update_record | 
set_hostname_cloud | Set the hostname on a VM and update cloud.cfg

### docker pack

#### Sensors

Name | Description
---- | -----------
DockerSensor | Docker sensor

#### Actions

Name | Description
---- | -----------
build_image | Build docker image action. Equivalent to docker build.

### dripstat pack

#### Sensors

Name | Description
---- | -----------
DripstatAlertSensor | Sensor which monitors Dripstat API for active alerts

### git pack

#### Sensors

Name | Description
---- | -----------
GitCommitSensor | Sensor which monitors git repository for new commits

#### Actions

Name | Description
---- | -----------
clone | Clone a repository

### github pack

#### Sensors

Name | Description
---- | -----------
GithubRepositorySensor | Sensor which monitors Github repository for activity

#### Actions

Name | Description
---- | -----------
add_comment | Add a comment to the provided issue / pull request.
add_status | Add a commit status for a provided ref.
get_clone_stats | Retrieve clone statistics for a given repository
get_traffic_stats | Retrieve traffic statistics for a given repository

### irc pack

#### Sensors

Name | Description
---- | -----------
IRCSensor | Sensor which monitors IRC and dispatches a trigger for each public and private message

### jira pack

#### Sensors

Name | Description
---- | -----------
JIRASensor | Sensor which monitors JIRA for new tickets

#### Actions

Name | Description
---- | -----------
create_issue | Create JIRA issue action.

### jmx pack

#### Sensors

Name | Description
---- | -----------
JMXSensor | Sensor which monitors Java application for attributes / metrics exposed through JMX protocol

### libcloud pack

#### Actions

Name | Description
---- | -----------
create_dns_record | Create a new DNS record.
create_vm | Create a new VM.
delete_dns_record | Delete an existing DNS record.
destroy_vm | Destroy a VM.
enable_cdn_for_container | Enable CDN for container and return the CDN URL
get_container_cdn_url | Retrieve CDN URL for existing CDN enabled container
get_object_cdn_url | Retrieve CDN URL for an object which is stored in a CDN enable container
import_public_ssh_key | Import an existing public SSH key.
list_dns_records | List available DNS records for a particular zone.
list_dns_zones | List available zones.
list_vms | List available VMs.
reboot_vm | Reboot a running VM.
start_vm | Start a new VM.
stop_vm | Stop a running VM.
upload_file | Upload a file to the provider container

### linux pack

#### Sensors

Name | Description
---- | -----------
FileWatchSensor | Sensor which monitors files for new lines

#### Actions

Name | Description
---- | -----------
check_loadavg | Check CPU Load Average on a Host
check_processes | Check Interesting Processes
cp | Copy file(s)
diag_loadavg | Diagnostic workflow for high load alert
dig | Dig action
file_touch | Touches a file
get_open_ports | Retrieve open ports for a given host
lsof | Run lsof
lsof_pids | Run lsof for a group of PIDs
mv | Move file(s)
netstat | Run netstat
netstat_grep | Grep netstat results
pkill | Kill processes using pkill
rm | Remove file(s)
rsync | Copy file(s) from one place to another w/ rsync
scp | Secure copy file(s)
service | Stops, Starts, or Restarts a service
traceroute | Traceroute a Host
vmstat | Run vmstat
wait_for_ssh | Wait for SSH

### newrelic pack

#### Actions

Name | Description
---- | -----------
get_alerts | Get alerts for app.
get_metric_data | Get metric data for metric.

### openstack pack

#### Actions

Name | Description
---- | -----------
cinder | Run OpenStack Cinder commands
get_instance_owners | Returns the users associated with a list of instance ids
glance | Run OpenStack Glance commands
nova | Run OpenStack Nova commands
nova_confirm | Confirms a resize or migrate
nova_instances | Returns a list of instances by hypervisor
nova_migrate_server | Evacuate guests from compute node

### puppet pack

#### Actions

Name | Description
---- | -----------
apply | Apply a standalone puppet manifest to a local system.
cert_clean | Revoke a host's certificate (if applicable) and remove all files related to that host from puppet cert's storage.
cert_revoke | Revoke the certificate of a client.
cert_sign | Sign an outstanding certificate request.
run_agent | Run puppet agent.

### sensu pack

#### Actions

Name | Description
---- | -----------
aggregate_list | List Sensu Aggregate Stats
check_aggregates | Get Sensu check aggregates
check_aggregates_delete | Delete Sensu check aggregates
check_aggregates_issued | Get a specific Sensu check aggregate
check_info | Get Sensu check info
check_list | List Sensu checks
check_request | Schedule a Sensu check request
client_delete | Delete a Sensu client
client_history | Get Sensu client history
client_info | Get Sensu client info
client_info | Get Sensu client info
client_list | List Sensu clients
event_client_list | List Sensu events for a given client
event_delete | Delete a Sensu event
event_info | Get Sensu event info
event_list | List Sensu events
health | Sensu System Health
info | Sensu System Info

### slack pack

#### Sensors

Name | Description
---- | -----------
SlackSensor | Sensor which monitors Slack for activity

#### Actions

Name | Description
---- | -----------
post_message | Post a message to the Slack channel.

### twilio pack

#### Actions

Name | Description
---- | -----------
send_sms | This sends a SMS using twilio.

### twitter pack

#### Sensors

Name | Description
---- | -----------
TwitterSearchSensor | Sensor which monitors twitter timeline for new tweets matching the specified criteria

## License, and Contributors Agreement

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
work except in compliance with the License. You may obtain a copy of the License in
the LICENSE file, or at
[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

By contributing you agree that these contributions are your own (or approved by
your employer) and you grant a full, complete, irrevocable copyright license to
all users and developers of the project, present and future, pursuant to the
license of the project.
