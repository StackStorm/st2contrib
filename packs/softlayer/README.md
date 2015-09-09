# Softlayer Integration Pack

Pack which allows integration with [Softlayer](https://www.softlayer.com/).

## Configuration

* ``username`` - Softlayer username.
* ``api_key`` - Api key.
* ``region`` - Not used yet, should be the default region you want to work with for instances.
* ``swift_region`` - Not used yet, will be the Softlayer Object Storage region to work with.

## Actions

* ``create_instance`` - Action which creates a new instance.
* ``destroy_instance`` - Action which destroys an existing instance.
* ``create_keypair`` - Action which creates a new keypair.
* ``delete_keypair`` - Action which deletes an existing keypair.