# Softlayer Integration Pack

Pack which allows integration with [Softlayer](https://www.softlayer.com/).

## Configuration

Copy the example configuration in [softlayer.yaml.example](./softlayer.yaml.example)
to `/opt/stackstorm/configs/softlayer.yaml` and edit as required.

It should contain:

* ``username`` - Softlayer username.
* ``api_key`` - Api key.
* ``region`` - Not used yet, should be the default region you want to work with for instances.
* ``swift_region`` - Not used yet, will be the Softlayer Object Storage region to work with.

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Actions

* ``create_instance`` - Action which creates a new instance.
* ``destroy_instance`` - Action which destroys an existing instance.
* ``create_keypair`` - Action which creates a new keypair.
* ``delete_keypair`` - Action which deletes an existing keypair.
