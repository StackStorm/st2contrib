# StackStorm Community Repo

[![StackStorm](https://github.com/stackstorm/st2/raw/master/stackstorm_logo.png)](http://www.stackstorm.com)

[![Build Status](https://travis-ci.org/StackStorm/st2contrib.svg?branch=master)](https://travis-ci.org/StackStorm/st2contrib)  [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/StackStorm/st2contrib/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/StackStorm/st2contrib/?branch=master)  [![IRC](https://img.shields.io/irc/%23stackstorm.png)](http://webchat.freenode.net/?channels=stackstorm)

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

Name | Description | Keywords | Author | Latest Version | Available Resources
---- | ----------- | -------- | ------ | -------------- | -------------------
| [ansible](https://github.com/StackStorm/st2contrib/tree/master/packs/ansible) | st2 content pack containing ansible integrations | ansible, cfg management, configuration management | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#ansible-pack)
| [aws](https://github.com/StackStorm/st2contrib/tree/master/packs/aws) | st2 content pack containing Amazon Web Services integrations. | aws, amazon web services, amazon, ec2, route53, cloud | [st2-dev](mailto:info@stackstorm.com) | 0.2 | [click](https://github.com/StackStorm/st2contrib#aws-pack)
| [azure](https://github.com/StackStorm/st2contrib/tree/master/packs/azure) | st2 content pack containing Microsoft Azure integrations. | microsoft, azure, cloud, libcloud, servers, virtual machines, azure virtual machines | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#azure-pack)
| [bitcoin](https://github.com/StackStorm/st2contrib/tree/master/packs/bitcoin) | bitcoin integration pack | bitcoin | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#bitcoin-pack)
| [chef](https://github.com/StackStorm/st2contrib/tree/master/packs/chef) | st2 chef integration pack | chef, chef-client, chef-solo, chef-apply, cfg management, configuration management, opscode | [st2-dev](mailto:info@stackstorm.com) | 0.1.1 | [click](https://github.com/StackStorm/st2contrib#chef-pack)
| [cubesensors](https://github.com/StackStorm/st2contrib/tree/master/packs/cubesensors) | st2 content pack containing CubeSensors integrations | cubesensors, iot, smart home, sensors, probes, home automation | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#cubesensors-pack)
| [docker](https://github.com/StackStorm/st2contrib/tree/master/packs/docker) | st2 content pack containing docker integrations | docker, containers, virtualization, cgroups | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#docker-pack)
| [dripstat](https://github.com/StackStorm/st2contrib/tree/master/packs/dripstat) | Integration with the Dripstat Application Performance Monitoring tool | dripstat, java, monitoring, performance monitoring | [James Fryman](mailto:james@fryman.io) | 0.0.1 | [click](https://github.com/StackStorm/st2contrib#dripstat-pack)
| [elasticsearch](https://github.com/StackStorm/st2contrib/tree/master/packs/elasticsearch) | st2 elasticsearch integration pack | elasticsearch, curator, databases | [st2-dev](mailto:info@stackstorm.com) | 0.1.2 | [click](https://github.com/StackStorm/st2contrib#elasticsearch-pack)
| [email](https://github.com/StackStorm/st2contrib/tree/master/packs/email) | E-Mail Actions/Sensors for StackStorm |  | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#email-pack)
| [fireeye](https://github.com/StackStorm/st2contrib/tree/master/packs/fireeye) | FireEye CM Series Integration |  | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#fireeye-pack)
| [git](https://github.com/StackStorm/st2contrib/tree/master/packs/git) | st2 content pack containing git integrations | git, scm | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#git-pack)
| [github](https://github.com/StackStorm/st2contrib/tree/master/packs/github) | st2 content pack containing github integrations | github, git, scm | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#github-pack)
| [google](https://github.com/StackStorm/st2contrib/tree/master/packs/google) | st2 content pack containing google integrations | google, search | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#google-pack)
| [gpg](https://github.com/StackStorm/st2contrib/tree/master/packs/gpg) | Pack for working with GPG. | gpg, pgp, gnupg, privacy, encryption, crypto | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#gpg-pack)
| [hubot](https://github.com/StackStorm/st2contrib/tree/master/packs/hubot) | Hubot integration pack |  | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#hubot-pack)
| [hue](https://github.com/StackStorm/st2contrib/tree/master/packs/hue) | Philips Hue Pack | hue, philips, iot | [James Fryman](mailto:james@stackstorm.com) | 0.0.1 | [click](https://github.com/StackStorm/st2contrib#hue-pack)
| [irc](https://github.com/StackStorm/st2contrib/tree/master/packs/irc) | st2 content pack containing irc integrations | irc, internet relay chat, chat, messaging, instant messaging | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#irc-pack)
| [jenkins](https://github.com/StackStorm/st2contrib/tree/master/packs/jenkins) | Jenkins CI Integration Pack |  | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#jenkins-pack)
| [jira](https://github.com/StackStorm/st2contrib/tree/master/packs/jira) | st2 content pack containing jira integrations | issues, ticket management, project management | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#jira-pack)
| [jmx](https://github.com/StackStorm/st2contrib/tree/master/packs/jmx) | st2 content pack containing Java JMX integrations | jmx, javajmx, java management extensions, mbean | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#jmx-pack)
| [lastline](https://github.com/StackStorm/st2contrib/tree/master/packs/lastline) | Lastline Security Breach Detection Integration |  | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#lastline-pack)
| [libcloud](https://github.com/StackStorm/st2contrib/tree/master/packs/libcloud) | st2 content pack containing libcloud integrations | libcloud, cloud, dns, dnsaas, lbaas, load balancers, aws, amazon, s3, ec2, rackspace, cloudstack, openstack, cloudsigma, gce, google compute engine | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#libcloud-pack)
| [mailgun](https://github.com/StackStorm/st2contrib/tree/master/packs/mailgun) | st2 content pack containing mailgun integrations | email, mail, mailgun | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#mailgun-pack)
| [mistral](https://github.com/StackStorm/st2contrib/tree/master/packs/mistral) | Mistral integrations to operate mistral. | mistral, workflows | [StackStorm](mailto:support@stackstorm.com) | 0.0.1 | [click](https://github.com/StackStorm/st2contrib#mistral-pack)
| [mmonit](https://github.com/StackStorm/st2contrib/tree/master/packs/mmonit) | st2 content pack containing mmonit integrations | monitoring, mmonit | [Itxaka Serrano Garcia](mailto:itxakaserrano@gmail.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#mmonit-pack)
| [mqtt](https://github.com/StackStorm/st2contrib/tree/master/packs/mqtt) | MQTT Integration for StackStorm |  | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#mqtt-pack)
| [nagios](https://github.com/StackStorm/st2contrib/tree/master/packs/nagios) | Nagios integration pack. See README.md for setup instructions. | nagios, monitoring, alerting | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#nagios-pack)
| [nest](https://github.com/StackStorm/st2contrib/tree/master/packs/nest) | StackStorm integration with Nest Thermostats |  | [James Fryman](mailto:james@stackstorm.com) | 0.0.1 | [click](https://github.com/StackStorm/st2contrib#nest-pack)
| [newrelic](https://github.com/StackStorm/st2contrib/tree/master/packs/newrelic) | st2 content pack containing newrelic integrations | new relic, monitoring, app monitoring, application level monitoring | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#newrelic-pack)
| [openhab](https://github.com/StackStorm/st2contrib/tree/master/packs/openhab) | Integration with OpenHAB | openhab, iot, smart home, home automation | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#openhab-pack)
| [openstack](https://github.com/StackStorm/st2contrib/tree/master/packs/openstack) | st2 content pack containing openstack integrations | cloud, nova, glance, neutron | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#openstack-pack)
| [pagerduty](https://github.com/StackStorm/st2contrib/tree/master/packs/pagerduty) | Packs which allows integration with PagerDuty services. |  | [Aamir](mailto:raza.aamir01@gmail.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#pagerduty-pack)
| [puppet](https://github.com/StackStorm/st2contrib/tree/master/packs/puppet) | st2 content pack containing puppet integrations | puppet, cfg management, configuration management | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#puppet-pack)
| [rabbitmq](https://github.com/StackStorm/st2contrib/tree/master/packs/rabbitmq) | st2 content pack containing rabbitmq integrations | rabbitmq, queuing, messaging, aqmp, stomp, message broker | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#rabbitmq-pack)
| [rackspace](https://github.com/StackStorm/st2contrib/tree/master/packs/rackspace) | Packs which allows integration with Rackspace services such as servers, load balancers and DNS. |  | [jfryman](mailto:jfryman@FryBook) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#rackspace-pack)
| [salt](https://github.com/StackStorm/st2contrib/tree/master/packs/salt) | st2 salt integration pack | salt, cfg management, configuration management | [jcockhren](mailto:jurnell@sophicware.com) | 0.3.1 | [click](https://github.com/StackStorm/st2contrib#salt-pack)
| [sensu](https://github.com/StackStorm/st2contrib/tree/master/packs/sensu) | st2 content pack containing sensu integrations | sensu, monitoring, alerting | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#sensu-pack)
| [slack](https://github.com/StackStorm/st2contrib/tree/master/packs/slack) | st2 content pack containing slack integrations | slack, chat, messaging, instant messaging | [st2-dev](mailto:info@stackstorm.com) | 0.1.1 | [click](https://github.com/StackStorm/st2contrib#slack-pack)
| [SmartThings](https://github.com/StackStorm/st2contrib/tree/master/packs/SmartThings) | Integration with SmartThings | smartthings, iot, smart home, home automation | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#SmartThings-pack)
| [softlayer](https://github.com/StackStorm/st2contrib/tree/master/packs/softlayer) | st2 content pack containing Softlayer integrations. | softlayer, cloud | [Itxaka Serrano Garcia](mailto:itxakaserrano@gmail.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#softlayer-pack)
| [st2](https://github.com/StackStorm/st2contrib/tree/master/packs/st2) | StackStorm pack management |  | [st2-dev](mailto:info@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#st2-pack)
| [Travis CI](https://github.com/StackStorm/st2contrib/tree/master/packs/Travis CI) | Pack which allows integration with Travis CI. | travis, travis ci, continous integration, ci | [Aamir](mailto:raza.aamir01@gmail.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#Travis CI-pack)
| [trello](https://github.com/StackStorm/st2contrib/tree/master/packs/trello) | Integration with Trello, Web based Project Management | trello, kanban, productivity, collaboration | [James Fryman](mailto:james@stackstorm.com) | 0.0.1 | [click](https://github.com/StackStorm/st2contrib#trello-pack)
| [twilio](https://github.com/StackStorm/st2contrib/tree/master/packs/twilio) | st2 content pack containing twilio integrations |  | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#twilio-pack)
| [twitter](https://github.com/StackStorm/st2contrib/tree/master/packs/twitter) | st2 content pack containing twitter integrations | twitter, social media, social networks | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#twitter-pack)
| [urbandict](https://github.com/StackStorm/st2contrib/tree/master/packs/urbandict) | st2 content pack containing urban dictionary integrations | urban dict, urban dictionary, puns | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#urbandict-pack)
| [Victorops](https://github.com/StackStorm/st2contrib/tree/master/packs/Victorops) | Packs which allows integration with Victorops events. | victorps integration, open, ack and resolve incidents | [Aamir](mailto:raza.aamir01@gmail.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#Victorops-pack)
| [webpagetest](https://github.com/StackStorm/st2contrib/tree/master/packs/webpagetest) | st2 content pack containing webpagetest integrations | webpagetest, benchmarking | [Linuturk](mailto:linuturk@onitato.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#webpagetest-pack)
| [windows](https://github.com/StackStorm/st2contrib/tree/master/packs/windows) | st2 content pack containing windows integrations | windows, wmi, windows management interface, wql | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#windows-pack)
| [witai](https://github.com/StackStorm/st2contrib/tree/master/packs/witai) | Wit AI Integration with StackStorm |  | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#witai-pack)
### ansible pack

#### Actions

Name | Description
---- | -----------
command | Run ad-hoc ansible command (module)
command_local | Run ad-hoc ansible command (module) on local machine
galaxy.install | Download & Install role from ansible galaxy
galaxy.list | Display a list of installed roles from ansible galaxy
galaxy.remove | Remove an installed from ansible galaxy role
playbook | Run ansible playbook
vault.decrypt | Decrypt ansible data files
vault.encrypt | Encrypt ansible data files

### aws pack

#### Sensors

Name | Description
---- | -----------
ServiceNotificationsSensor | Sensor which exposes an HTTP interface and listens for AWS service notifications delivered via AWS SNS

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

### azure pack

#### Actions

Name | Description
---- | -----------
create_container | Create a new storage container.
create_vm | Create a new VM.
delete_container | Delete a storage container.
delete_object | Delete an object.
destroy_vm | Destroy a VM.
list_container_objects | List storage objects for the provided container.
list_containers | List storage containers.
list_vms | List available VMs.
reboot_vm | Reboot a running VM.
upload_file | Upload a file to the provided container.

### bitcoin pack

#### Actions

Name | Description
---- | -----------
getaccountaddress | Retrieves address of local wallet.
getwalletinfo | Information of the local wallet.
sendtoaddresss | Send some BTC to supplied address.

### chef pack

#### Actions

Name | Description
---- | -----------
apply | Performs one-off resource converge on remote hosts.
client | Performs chef-client run on remote hosts.
install | Performs installation of chef-client on remote nodes
ohai | Performs chef-solo run on remote hosts.
solo | Performs chef-solo run on remote hosts.

### cubesensors pack

#### Sensors

Name | Description
---- | -----------
CubeSensorsMeasurementsSensor | Sensor which polls CubeSensors API for new measurements and dispatch a trigger every time a new measurement is detected.

#### Actions

Name | Description
---- | -----------
get_device | Retrieve details for a particular device (cube).
get_measurements | Retrieve current measurements for a particular device (cube).
list_devices | List information about all the available devices (cubes).

### docker pack

#### Sensors

Name | Description
---- | -----------
DockerSensor | Docker sensor

#### Actions

Name | Description
---- | -----------
build_image | Build docker image action. Equivalent to docker build.
pull_image | Pull docker image action. Equivalent to docker pull.
push_image | Push docker image action. Equivalent to docker push.

### dripstat pack

#### Sensors

Name | Description
---- | -----------
DripstatAlertSensor | Sensor which monitors Dripstat API for active alerts

### elasticsearch pack

#### Actions

Name | Description
---- | -----------
indices.alias | Index Aliasing
indices.allocation | Index Allocation
indices.bloom | Disable bloom filter cache
indices.close | Close indices
indices.delete | Delete indices
indices.open | Open indices
indices.optimize | Optimize indices
indices.replicas | Replica Count Per-shard
indices.show | Show indices
indices.snapshot | Create snapshot of indices
search.body | Search query (full body)
search.q | Search query (lucene syntax)
snapshots.delete | Delete snapshots
snapshots.show | Show snapshots

### email pack

#### Sensors

Name | Description
---- | -----------
IMAPSensor | Sensor that emits triggers when e-mail message is received via IMAP
SMTPSensor | Sensor that emits triggers when e-mail message is received via SMTP

### fireeye pack

#### Actions

Name | Description
---- | -----------
get_alert_query | Request existing alert profiles with optional filters
get_submission_results | Query results of completed job
get_submission_status | Query status of running job
submit_malware | Submit a Malware object to FireEye AX appliance
view_ax_config | Returns a list of profiles and applications on AX devices

### git pack

#### Sensors

Name | Description
---- | -----------
GitCommitSensor | Sensor which monitors git repository for new commits

#### Actions

Name | Description
---- | -----------
clone | Clone a repository
get_local_repo_latest_commit | Retrieve SHA of the latest commit for the provided branch in a local repository.
get_remote_repo_latest_commit | Retrieve SHA of the latest commit for the provided branch in a remote repository.

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
get_issue | Retrieve information about a particular Github issue.
get_traffic_stats | Retrieve traffic statistics for a given repository

### google pack

#### Actions

Name | Description
---- | -----------
get_search_results | Retrieve Google search results for the provided query.

### gpg pack

#### Actions

Name | Description
---- | -----------
decrypt_file | Decrypt asymmetrically encrypted GPG file.
encrypt_file | Encrypt a file using asymmetric encryption for the provided recipients.
import_keys | Import keys into the keyring.
list_keys | List all keys in the keyring.

### hubot pack

#### Actions

Name | Description
---- | -----------
branch | Determine which branch Hubot is currently running
deploy | Manage Hubot installs on a per-pack basis
post_message | Post a message to Hubot
post_result | Post an execution result to Hubot
restart | Restart hubot
update_ref | Manage Hubot installs on a per-pack basis

### hue pack

#### Actions

Name | Description
---- | -----------
alert | Send an alert to a light
brightness | Change the brightness of a bulb
color_temp_kelvin | Change the bulb color temperature to a specific temperature in Kelvin
color_temp_mired | Change the bulb color temperature to a specific temperature in mired scale
current_state | Get current state of bridge
find_id_by_name | Find bulb ID based on nickname
list_bulbs | List all registered bulbs
off | Turn off a bulb
on | Turn on a bulb
rgb | Change bulb color based on RGB Values
set_state | Send manual state to bulb
toggle | Toggle on/off state of a bulb
xy | Change bulb color based on CIE color space values

### irc pack

#### Sensors

Name | Description
---- | -----------
IRCSensor | Sensor which monitors IRC and dispatches a trigger for each public and private message

### jenkins pack

#### Actions

Name | Description
---- | -----------
build_job | Kick off Jenkins Build Jobs
list_running_jobs | List currently running Jenkins jobs

### jira pack

#### Sensors

Name | Description
---- | -----------
JIRASensor | Sensor which monitors JIRA for new tickets

#### Actions

Name | Description
---- | -----------
create_issue | Create a new JIRA issue / ticket.
get_issue | Retrieve information about a particular JIRA issue.

### jmx pack

#### Sensors

Name | Description
---- | -----------
JMXSensor | Sensor which monitors Java application for attributes / metrics exposed through JMX protocol

#### Actions

Name | Description
---- | -----------
invoke_method | Invoke a provided MBean method exposed over JMX.

### lastline pack

#### Actions

Name | Description
---- | -----------
get_completed | Get artifact generated by an analysis result for a previously submitted analysis task.
get_progress | Get a progress estimate for a previously submitted analysis task.
get_result | Get results for a previously submitted analysis task.
get_result_artifact | Get artifact generated by an analysis result for a previously submitted analysis task.
get_result_summary | Get result summary for a previously submitted analysis task.
submit_file | Submit a file to Lastline for analysis
submit_file_hash | Submit a file hash to Lastline for analysis
submit_url | Submit a URL for analysis to Lastline

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
upload_file | Upload a file to the provided container

### mailgun pack

#### Actions

Name | Description
---- | -----------
send_email | Send email via Mailgun HTTP API.

### mistral pack

#### Actions

Name | Description
---- | -----------
get_task_results | Get results of mistral task in an execution.
get_workbook_definition | Get the definition of the mistral workbook.
get_workflow_results | Get results of mistral workflow.
kill_workflow | Kill a running mistral workflow.

### mmonit pack

#### Sensors

Name | Description
---- | -----------
MmonitEventsSensor | Sensor which monitors mmonit for events

#### Actions

Name | Description
---- | -----------
action_host | Performs the specified action for the selected host services.
delete_host | Returns details for the given host id.
dismiss_event | Dismiss the given active event so it doesn't show up in the event list if active filter is set to 2.
get_event | Returns details for a specific event.
get_host | Returns details for the given host id.
get_status_host | Returns detailed status of the given host.
get_uptime_hosts | Returns services uptime for a particular host.
list_events | Returns a list of events stored in M/Monit.
list_hosts | Returns a list of all hosts registered in M/Monit.
list_status_hosts | Returns the current status of all hosts registered in M/Monit.
list_uptime_hosts | Returns hosts uptime overview. If a custom range is used, the difference between datefrom and dateto should be in minutes, not in seconds since 1 minute is the lowest data resolution in M/Monit.
session_delete | Delete session attributes matching key. If no keys were specified, delete all stored attributes.
session_get | Returns the session attribute matching the session_key argument. If no keys are specified, all stored attributes in the session are returned.
session_put | Add or update the session attribute. If a named attribute already exist, its old value is replaced.
summary_events | Returns the events summary for the last 24 hours.
summary_status | Returns a status summary of all hosts.
test_connection_to_host | Checks that M/Monit can connect to the host with the given network settings.
update_host | Updates the host settings in the M/Monit database.

### mqtt pack

#### Sensors

Name | Description
---- | -----------
MQTTSensor | Listen for events on MQTT bus/topic

#### Actions

Name | Description
---- | -----------
publish | Publish message to MQTT broker

### nest pack

#### Actions

Name | Description
---- | -----------
get_humidity | Get the current humidity
get_mode | Manage nest modes
get_temperature | Get the current temperature.
set_away | Set nest to away mode
set_fan | Manage fan state
set_home | Set nest to home mode
set_humidity | Set humidity goal for nest
set_mode | Set current operating mode
set_temperature | Set current temperature.
show | Show current Nest information
toggle_away | Toggle current Home/Away status

### newrelic pack

#### Sensors

Name | Description
---- | -----------
NewRelicHookSensor | Sensor which watches for alerts from NewRelic.

#### Actions

Name | Description
---- | -----------
get_alerts | Get alerts for app.
get_metric_data | Get metric data for metric.

### openhab pack

#### Actions

Name | Description
---- | -----------
get_status | Get status on an item
send_command | Send a command to an item
set_state | Set state on an item

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

### pagerduty pack

#### Actions

Name | Description
---- | -----------
ack_incident | ACK an incident on PagerDuty
get_open_incidents | Retrive list of open incidents from PagerDuty
launch_incident | Launch an incident on PagerDuty
resolve_incident | Resolve an incident whose key is provided

### puppet pack

#### Actions

Name | Description
---- | -----------
apply | Apply a standalone puppet manifest to a local system.
cert_clean | Revoke a host's certificate (if applicable) and remove all files related to that host from puppet cert's storage.
cert_revoke | Revoke the certificate of a client.
cert_sign | Sign an outstanding certificate request.
run_agent | Run puppet agent.

### rabbitmq pack

#### Sensors

Name | Description
---- | -----------
RabbitMQSensor | Sensor which monitors a RabbitMQ queue for new messages

#### Actions

Name | Description
---- | -----------
list_exchanges | List RabbitMQ exchanges
list_queues | List RabbitMQ queues
publish_message | Publish a message in RabbitMQ

### rackspace pack

#### Actions

Name | Description
---- | -----------
add_node_to_loadbalancer | Add a new node to load balancer
create_dns_record | Create a new DNS record.
create_dns_zone | Create a new DNS zone.
create_loadbalancer | Create a new loadbalancer.
create_vm | Create a new VM / cloud server
delete_dns_record | Delete a DNS record.
delete_dns_zone | Delete a DNS zone.
delete_loadbalancer | Delete a loadbalancer
delete_node_from_loadbalancer | Delete a node from a load balancer
delete_vm | Delete a vm.
find_dns_record_id | Find a DNS record ID based on name
find_dns_zone_id | Find a DNS zone id based on name
find_loadbalancer_id | Find a loadbalancer id based on name
find_vm_id | Find a virtual machine id based on name
get_vm_by_ip | Retrieve information for a VM which matches the provided public IP.
get_vm_ids | Retrieve IDs for all the available VMs. Optionally filter by metadata and count.
get_vm_info | Retrieve information for a provided VM. Optionally filter on the metadata values.
get_vm_ips | Retrieve public IP addresses for all the available VMs. Optionally filter by metadata and count.
get_vm_names | List all the available vms by names. Optionally filter by metadata and count
list_dns_records | List all records for a particular zone.
list_dns_zones | List all the DNS zones.
list_vm_images | List all the available VM images
list_vm_sizes | List all the available VM sizes
list_vms | List all the available vms. Optionally filter on the metadata values.
set_vm_metadata | Set metadata values for the provided VM.
set_vm_metadata_item | Set a value of a metadata item for a provided VM.

### salt pack

#### Actions

Name | Description
---- | -----------
bootstrap | Bootstrap servers with salt.cloud runner
client | Run salt LocalClient functions
local | Run Salt Exection Modules through Salt API
local_archive.gunzip | Run Salt Execution modules through Salt API
local_archive.gzip | Run Salt Execution modules through Salt API
local_archive.rar | Run Salt Execution modules through Salt API
local_archive.tar | Run Salt Execution modules through Salt API
local_archive.unrar | Run Salt Execution modules through Salt API
local_archive.unzip | Run Salt Execution modules through Salt API
local_archive.zip_ | Run Salt Execution modules through Salt API
local_cloud.action | Run Salt Execution modules through Salt API
local_cloud.create | Run Salt Execution modules through Salt API
local_cloud.destroy | Run Salt Execution modules through Salt API
local_cloud.network_create | Run Salt Execution modules through Salt API
local_cloud.profile_ | Run Salt Execution modules through Salt API
local_cloud.virtual_interface_create | Run Salt Execution modules through Salt API
local_cloud.volume_attach | Run Salt Execution modules through Salt API
local_cloud.volume_create | Run Salt Execution modules through Salt API
local_cloud.volume_delete | Run Salt Execution modules through Salt API
local_cloud.volume_detach | Run Salt Execution modules through Salt API
local_cmdmod.run | Run Salt Execution modules through Salt API
local_cmdmod.run_chroot | Run Salt Execution modules through Salt API
local_cmdmod.script | Run Salt Execution modules through Salt API
local_cp.get_file | Run Salt Execution modules through Salt API
local_cp.get_url | Run Salt Execution modules through Salt API
local_cp.push | Run Salt Execution modules through Salt API
local_cp.push_dir | Run Salt Execution modules through Salt API
local_cron.ls | Run Salt Execution modules through Salt API
local_cron.rm_env | Run Salt Execution modules through Salt API
local_cron.rm_job | Run Salt Execution modules through Salt API
local_cron.set_env | Run Salt Execution modules through Salt API
local_cron.set_job | Run Salt Execution modules through Salt API
local_data.cas | Run Salt Execution modules through Salt API
local_data.dump | Run Salt Execution modules through Salt API
local_data.getval | Run Salt Execution modules through Salt API
local_data.update | Run Salt Execution modules through Salt API
local_event.fire | Run Salt Execution modules through Salt API
local_event.fire_master | Run Salt Execution modules through Salt API
local_event.send | Run Salt Execution modules through Salt API
local_file.access | Run Salt Execution modules through Salt API
local_file.chgrp | Run Salt Execution modules through Salt API
local_file.chown | Run Salt Execution modules through Salt API
local_file.directory_exists | Run Salt Execution modules through Salt API
local_file.file_exists | Run Salt Execution modules through Salt API
local_file.find | Run Salt Execution modules through Salt API
local_file.manage_file | Run Salt Execution modules through Salt API
local_file.mkdir | Run Salt Execution modules through Salt API
local_file.remove | Run Salt Execution modules through Salt API
local_file.replace | Run Salt Execution modules through Salt API
local_file.search | Run Salt Execution modules through Salt API
local_file.symlink | Run Salt Execution modules through Salt API
local_file.touch | Run Salt Execution modules through Salt API
local_file.truncate | Run Salt Execution modules through Salt API
local_grains.append | Run Salt Execution modules through Salt API
local_grains.delval | Run Salt Execution modules through Salt API
local_grains.get | Run Salt Execution modules through Salt API
local_grains.remove | Run Salt Execution modules through Salt API
local_grains.setval | Run Salt Execution modules through Salt API
local_hosts.add_hosts | Run Salt Execution modules through Salt API
local_hosts.get_alias | Run Salt Execution modules through Salt API
local_hosts.get_ip | Run Salt Execution modules through Salt API
local_hosts.rm_host | Run Salt Execution modules through Salt API
local_hosts.set_host | Run Salt Execution modules through Salt API
local_htpasswd.useradd | Run Salt Execution modules through Salt API
local_htpasswd.userdel | Run Salt Execution modules through Salt API
local_mine.delete | Run Salt Execution modules through Salt API
local_mine.get | Run Salt Execution modules through Salt API
local_mine.send | Run Salt Execution modules through Salt API
local_mine.update | Run Salt Execution modules through Salt API
local_network.connect | Run Salt Execution modules through Salt API
local_network.interface_ip | Run Salt Execution modules through Salt API
local_network.ipaddrs | Run Salt Execution modules through Salt API
local_network.ping | Run Salt Execution modules through Salt API
local_network.subnets | Run Salt Execution modules through Salt API
local_pillar.get | Run Salt Execution modules through Salt API
local_pip.freeze | Run Salt Execution modules through Salt API
local_pip.install | Run Salt Execution modules through Salt API
local_pip.uninstall | Run Salt Execution modules through Salt API
local_pkg.install | Run Salt Execution modules through Salt API
local_pkg.refresh_db | Run Salt Execution modules through Salt API
local_pkg.remove | Run Salt Execution modules through Salt API
local_puppet.disable | Run Salt Execution modules through Salt API
local_puppet.enable | Run Salt Execution modules through Salt API
local_puppet.fact | Run Salt Execution modules through Salt API
local_puppet.noop | Run Salt Execution modules through Salt API
local_puppet.run | Run Salt Execution modules through Salt API
local_puppet.status | Run Salt Execution modules through Salt API
local_puppet.summary | Run Salt Execution modules through Salt API
local_ret.get_fun | Run Salt Execution modules through Salt API
local_ret.get_jid | Run Salt Execution modules through Salt API
local_ret.get_jids | Run Salt Execution modules through Salt API
local_ret.get_minions | Run Salt Execution modules through Salt API
local_saltutil.sync_all | Run Salt Execution modules through Salt API
local_saltutil.sync_grains | Run Salt Execution modules through Salt API
local_saltutil.sync_modules | Run Salt Execution modules through Salt API
local_saltutil.sync_outputters | Run Salt Execution modules through Salt API
local_saltutil.sync_renderers | Run Salt Execution modules through Salt API
local_saltutil.sync_returners | Run Salt Execution modules through Salt API
local_saltutil.sync_states | Run Salt Execution modules through Salt API
local_saltutil.sync_utils | Run Salt Execution modules through Salt API
local_schedule.add | Run Salt Execution modules through Salt API
local_schedule.delete | Run Salt Execution modules through Salt API
local_schedule.disable_job | Run Salt Execution modules through Salt API
local_schedule.enable_job | Run Salt Execution modules through Salt API
local_schedule.run_job | Run Salt Execution modules through Salt API
local_service.available | Run Salt Execution modules through Salt API
local_service.restart | Run Salt Execution modules through Salt API
local_service.start | Run Salt Execution modules through Salt API
local_service.status | Run Salt Execution modules through Salt API
local_service.stop | Run Salt Execution modules through Salt API
local_shadow.del_password | Run Salt Execution modules through Salt API
local_shadow.gen_password | Run Salt Execution modules through Salt API
local_shadow.set_expire | Run Salt Execution modules through Salt API
local_state.highstate | Run Salt Execution modules through Salt API
local_state.single | Run Salt Execution modules through Salt API
local_state.sls | Run Salt Execution modules through Salt API
local_supervisord.add | Run Salt Execution modules through Salt API
local_supervisord.custom | Run Salt Execution modules through Salt API
local_supervisord.remove | Run Salt Execution modules through Salt API
local_supervisord.reread | Run Salt Execution modules through Salt API
local_supervisord.restart | Run Salt Execution modules through Salt API
local_supervisord.start | Run Salt Execution modules through Salt API
local_supervisord.stop | Run Salt Execution modules through Salt API
local_systemd.available | Run Salt Execution modules through Salt API
local_systemd.disable | Run Salt Execution modules through Salt API
local_systemd.enable | Run Salt Execution modules through Salt API
local_systemd.restart | Run Salt Execution modules through Salt API
local_systemd.start | Run Salt Execution modules through Salt API
local_systemd.stop | Run Salt Execution modules through Salt API
local_systemd.systemctl_reload | Run Salt Execution modules through Salt API
local_test.cross_test | Run Salt Execution modules through Salt API
local_test.echo | Run Salt Execution modules through Salt API
local_test.ping | Run Salt Execution modules through Salt API
local_useradd.add | Run Salt Execution modules through Salt API
local_useradd.chshell | Run Salt Execution modules through Salt API
local_useradd.delete | Run Salt Execution modules through Salt API
runner | Run Salt Runner functions through Salt API
runner_cache.clear_all | Run Salt Runner functions through Salt API
runner_cache.clear_grains | Run Salt Runner functions through Salt API
runner_cache.clear_mine | Run Salt Runner functions through Salt API
runner_cache.clear_mine_func | Run Salt Runner functions through Salt API
runner_cache.clear_pillar | Run Salt Runner functions through Salt API
runner_cache.grains | Run Salt Runner functions through Salt API
runner_cache.mine | Run Salt Runner functions through Salt API
runner_cache.pillar | Run Salt Runner functions through Salt API
runner_cloud.action | Run Salt Runner functions through Salt API
runner_cloud.full_query | Run Salt Runner functions through Salt API
runner_cloud.list_images | Run Salt Runner functions through Salt API
runner_cloud.list_locations | Run Salt Runner functions through Salt API
runner_cloud.list_sizes | Run Salt Runner functions through Salt API
runner_cloud.profile | Run Salt Runner functions through Salt API
runner_cloud.query | Run Salt Runner functions through Salt API
runner_cloud.select_query | Run Salt Runner functions through Salt API
runner_jobs.active | Run Salt Runner functions through Salt API
runner_jobs.list_jobs | Run Salt Runner functions through Salt API
runner_manage.down | Run Salt Runner functions through Salt API
runner_manage.status | Run Salt Runner functions through Salt API
runner_manage.up | Run Salt Runner functions through Salt API
runner_manage.versions | Run Salt Runner functions through Salt API
runner_pillar.show_pillar | Run Salt Runner functions through Salt API
runner_pillar.show_top | Run Salt Runner functions through Salt API
runner_thin.generate | Run Salt Runner functions through Salt API

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

### smartthings pack

#### Sensors

Name | Description
---- | -----------
SmartThingsSensor | Sensor listening for HTTP events from SmartThings

#### Actions

Name | Description
---- | -----------
command | Send a generic command to a device
disengage_lock | Disengage (lock) a device that can be locked
engage_lock | Engage (lock) a device that can be locked
find_id_by_name | Lookup a specific device ID based on its name/type
get_device_info | Get information on a specific device
list_devices | List devices of a specific type from SmartThings
set_mode | Set current temperature.
set_temperature | Set current temperature.
toggle_lock | Toggle a lock
toggle_switch | Toggle a switch
turn_off_switch | Turn off a light
turn_on_switch | Turn on a switch

### softlayer pack

#### Actions

Name | Description
---- | -----------
create_instance | Creates a new instance
create_keypair | Creates a keypair by name
delete_keypair | Deletes a keypair by name. If there are mutiple keys with the same name it will only delete the first
destroy_instance | Destroys an instance

### st2 pack

#### Actions

Name | Description
---- | -----------
actions.list | Retrieve a list of available StackStorm actions.
call_home | Sends anonymous data install data to a StackStorm write-only S3 dropbox
executions.get | Retrieve details of a single execution.
executions.list | Retrieve a list of executions.
executions.re_run | Re-run an action execution.
kv.delete | Delete value from datastore
kv.get | Get value from datastore
kv.get_object | Deserialize and retrieve JSON serialized object from a datastore
kv.grep | Grep for values in datastore
kv.set | Set value in datastore
kv.set_object | Serialize and store object in a datastore
rules.list | Retrieve a list of available StackStorm rules
sensors.list | Retrieve a list of available StackStorm sensors.
upload_to_s3 | Sends collected data to write-only StackStorm S3 bucket

### travis_ci pack

#### Actions

Name | Description
---- | -----------
cancel_build | Cancel a build.
disable_hook | Disable hooks for a git repo.
enable_hook | Enable hook for a git repo.
get_repo | Retrieve details for a provided repository.
list_branches | List all branches for a given repository.
list_builds | List details of all the available builds.
list_hooks | List available hooks for the authenticated user.
list_repos | List repositories for the provided user.
restart_build | Restart a Build

### trello pack

#### Actions

Name | Description
---- | -----------
add_board | Create a new board
add_card | Add a new card to a list
add_list | Add a new list to a board
close_board | Close a board
close_card | Close a card
close_list | Close a list belonging to a board
find_board_by_name | Lookup a board ID based on name. Returns one or more IDs
find_card_by_name | Lookup a Card ID based on name. Returns one or more IDs
find_list_by_name | Lookup a list ID based on name. Returns one or more IDs
move_card | Move a card from one board/list to another board/list
view_boards | Return a dictionary of all boards and their IDs
view_cards | View all cards on a board
view_lists | View all lists belonging to a board
view_organizations | List all organizations for user

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

#### Actions

Name | Description
---- | -----------
direct_message | Direct message a user.
follow | Follow a user.
update_status | Update your status (post a new tweet).

### urbandict pack

#### Actions

Name | Description
---- | -----------
get_definitions | Retrieve definitions from urbandict for the provided term.

### victorops pack

#### Actions

Name | Description
---- | -----------
ack_incident | Acknowledge a triggered event on victorops
open_incident | Triggers the event on VictorOps with the given parameters
recover_incident | Recover a triggered event on victorops

### webpagetest pack

#### Actions

Name | Description
---- | -----------
list_locations | List available testing locations.
random_test | Test a domain on WebPageTest from a random location.
request_test | Test a domain on WebPageTest.

### windows pack

#### Actions

Name | Description
---- | -----------
wmi_query | Run a WMI query on a particular Windows host.

### witai pack

#### Actions

Name | Description
---- | -----------
text_query | Send a text query to Wit.ai API

## License, and Contributors Agreement

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
work except in compliance with the License. You may obtain a copy of the License in
the LICENSE file, or at
[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

By contributing you agree that these contributions are your own (or approved by
your employer) and you grant a full, complete, irrevocable copyright license to
all users and developers of the project, present and future, pursuant to the
license of the project.
