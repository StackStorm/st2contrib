# Librato Integration Pack

This pack allows for Librato integrations.

## Configuration

Copy the example configuration in [librato.yaml.example](./librato.yaml.example)
to `/opt/stackstorm/configs/librato.yaml` and edit as required.

It must contain:

* ``user`` - Librato token
* ``token`` - Librato token

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Actions

* ``add_annotation``
* ``delete_metric``
* ``get_metric``
* ``list_metrics``
* ``submit_counter``
* ``submit_gauge``
