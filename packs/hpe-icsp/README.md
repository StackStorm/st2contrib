# HPE Insight Control Server Provisioning Integration Pack

Pack to communicate with HPE's Insight Control Server Provisioning Application. Allows for the assignment of buildplans to stream OS Installations 

## Connection Configuration

Default Connection details can be specified within the `config.yaml`. These values can be overriden using the connection_data flow parameter.

```yaml
  host:
  user:
  pass:
  apiv: 102
  sslverify: True
```
Each element of the above can be independently overridden using the "connection_data" object parameter for each action.

## Usage considerations
### API Versions
API versions use different variable names. One known api variation is "hostname". This is used within the buildplan assignment api call.
Between versions the case of some characters within the variable name has changed:
* 102: hostname
* 108: hostName
using an incorrect match of version and variable will results in the api call reporting in correct json elements. Given that the provided buildplans utilise the 102 format of hostname, actions within this pack are designed to work with the 102 version of the api.
To increase the version number to a later release will require updates to actions and buildplans.

## TODO
* Extend build plan application action to include network configuration information

## Actions

* `hpe-icsp.icsp_server_attributes_get` - Retrieve attributes set against server
* `hpe-icsp.icsp_server_attributes_set` - Assign custom cttributes to server
* `hpe-icsp.icsp_buildplan_apply` - Assign build plans provided against list of servers
* `hpe-icsp.icsp_buildplan_get` - Retrieve list of Build plans and Build Plan URIs
* `hpe-icsp.icsp_job_status` - Retrieve Status of specified Job
* `hpe-icsp.icsp_mid_get` - Retrieve ICSP ID (MID) for Specified Server
* `hpe-icsp.icsp_server_delete` - Remove server record from ICSP instance
