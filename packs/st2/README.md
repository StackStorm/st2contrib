# StackStorm Integration Pack

The super-meta package! This integration allows integration with StackStorm.

Requires StackStorm >= `v0.8.0`

## Configuration:

* `base_url` - Base URL for the StackStorm API server endpoints (i.e.
  ``http://localhost``). If only the base URL is provided, the client will
  assume default ports for the API servers are used. If any of the API server
  URL is provided, it will override the base URL and default port.

## Actions

* ``kv.get`` - Retrieve string value from a datastore.
* ``kv.set`` - Store string value in a datastore.
* ``kv.grep`` - Find datastore items which name matches the provided query.
* ``kv.delete`` - Delete item from a datastore.

* ``kv.get_object`` - Deserialize and retrieve JSON serialized object from a
  datastore.
* ``kv.set_object`` - Serialize and store object in a datastore. Note: object
  is serialized as JSON.
