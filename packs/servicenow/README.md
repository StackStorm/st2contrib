# ServiceNow Integration Pack

This integration allows bi-directional communication between StackStorm and ServiceNow REST API

# Overview

This action provides the basic REST primitives necessary to allow communication between StackStorm and ServiceNow. Ideally, this integration will be consumed in a site-specific integration pack that defines actions to specific ServiceNow specific business logic.

ServiceNow provides two videos to demonstrate how to setup Inbound and Outbound Web Service integrations.

* Inbound Integration - https://www.youtube.com/watch?v=EhxgEECd7mQ
* Outbound Integration - https://www.youtube.com/watch?v=WeeDW_iRM8k

An example pack has been included in this pack to show the integration of ServiceNow with these two integration examples.

# Setup
## Configuration

### Outgoing Integration

* `instance_name` - Upstream Instance Name (e.x.: stackstorm)
* `username` - Username of service account
* `password` - Password of service account

### Incoming Integration

In your ServiceNow Outbound integration, REST endpoints accept JSON payloads. In addition, you must specify the following headers in your payload request:

```
Accept: application/json
Content-Type: application/json
```


## Actions

* `servicenow.get` - Get an entry from a ServiceNow Table
* `servicenow.update` - Update an entry in a ServiceNow Table
* `servicenow.insert` - Insert an entry to a ServiceNow Table
* `servicenow.delete` - Delete an entry from a ServiceNow Table
