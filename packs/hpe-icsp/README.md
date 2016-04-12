# HPE Insight Control Server Provisioning Integration Pack

Pack to communicate with HPE Insight Control Server Provisioning Application. Allows for the assignment of buildplans to stream OS Installations 

## Connection Configuration

Defaut Connection details can be specified within the `config.yaml`. These values can be overriden using the connection_data flow parameter.

```yaml
  host:
  user:
  pass:
  apiv: 104
  sslverify: True
```

To retrieve apiv, retrieve your ICSP version
```
https://ICSP/rest/version
```

### Override Connection configuration
Host, user and password can be individually overridden via the use of the "connection_detail" parameter.
```
  {
    "host": "192.168.0.1",
    "user": "username",
    "pass": "secret" 
  } 
```
Each attribute is independant allowing a mixture of config.yaml and parameter to be used as suits.

## Actions

* `hpe-icsp.icsp_server_attributes_get` - Retrieve attributes set against server
* `hpe-icsp.icsp_server_attributes_set` - Assign custom cttributes to server
* `hpe-icsp.icsp_buildplan_apply` - Assign build plans provided against list of servers
* `hpe-icsp.icsp_buildplan_get` - Retrieve list of Build plans and Build Plan URIs
* `hpe-icsp.icsp_job_status` - Retrieve Status of specified Job
* `hpe-icsp.icsp_mid_get` - Retrieve ICSP ID (MID) for Specified Server
* `hpe-icsp.icsp_server_delete` - Remove server record from ICSP instance
