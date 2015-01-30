# StackStorm Integration Pack

The super-meta package! This integration allows integration with StackStorm. 

Requires StackStorm <= `v0.8.0`

## Configuration:

* `base_url` - Base URL for the StackStorm API server endpoints (i.e. http://localhost). If only the base URL is provided, the client will assume default ports for the API servers are used. If any of the API server URL is provided, it will override the base URL and default port.

## Actions

* `kvstore` - Manipulate the key/value datastore (create/update/delete)
