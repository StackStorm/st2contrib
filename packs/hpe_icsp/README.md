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
using an incorrect match of version and variable will results in the api call reporting incorrect json elements. Given that the provided buildplans utilise the 102 format of hostname, actions within this pack are designed to work with the 102 version of the api.
To increase the version number to a later release will require updates to actions and buildplans.

## TODO
* Extend build plan application action to include network configuration information
* Identify correct domain and workgroup names for json payload.

## Actions

* `hpe_icsp.icsp_buildplan_apply` - Assign build plans provided against list of servers
* `hpe_icsp.icsp_buildplan_get` - Retrieve list of Build plans and Build Plan URIs
* `hpe_icsp.icsp_ca_cert` - Retrieve certificate for ICSP server
* `hpe_icsp.icsp_ids_to_os` - Allow for the application of build plans to a list of Servers
* `hpe_icsp.icsp_job_status` - Retrieve Status of specified Job
* `hpe_icsp.icsp_mid_get` - Retrieve ICSP ID (MID) for Specified Server
* `hpe_icsp.icsp_multi_server_attribute_add` - Apply Attribute with server unique values across multiple servers.
* `hpe_icsp.icsp_server_attributes_add` - Assign custom cttributes to server
* `hpe_icsp.icsp_server_attributes_del` - Remove custom attribute from server
* `hpe_icsp.icsp_server_attributes_get` - Retrieve attributes set against server
* `hpe_icsp.icsp_server_data_format` - Generates the json object used in the buildplan apply action
* `hpe_icsp.icsp_server_delete` - Remove server record from ICSP instance
* `hpe_icsp.icsp_server_details_get` - Return Summary information on server
