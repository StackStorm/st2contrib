# HPE Insight Control Server Provisioning Integration Pack

Pack to communicate with HPE's Insight Control Server Provisioning Application. Allows for the assignment of buildplans to stream OS Installations 

## Connection Configuration

Defaut Connection details can be specified within the `config.yaml`. These values can be overriden using the connection_data flow parameter.

```yaml
  host:
  user:
  pass:
  apiv: 104
  sslverify: True
```

## Actions

* `hpe-icsp.icsp_server_attributes_get` - Retrieve all Server Attributes set against server
* `hpe-icsp.icsp_server_attributes_set` - Assign Custom Attributes to Server
* `hpe-icsp.icsp_buildplan_apply` - Assign build plans provided list of Servers
* `hpe-icsp.icsp_buildplan_get` - Retrieve list of Build plans and Build Plan IDs
* `hpe-icsp.icsp_job_status` - Retrieve Status of specified Job
* `hpe-icsp.icsp_mid_get` - Retrieve ICSP ID (MID) for Specified Server
* `hpe-icsp.icsp_server_delete` - Remove server record from ICSP instance
