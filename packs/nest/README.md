# Nest Thermostat Integration Pack

This integration pack allows you to integrate with
[Nest](https://nest.com) thermostat.

## Configuration

* `username` - Nest.com username
* `password` - Nest.com password
* `structure` - Default nest home ID to query (Default: 0)
* `device` - Default device ID to query (Default: 0)

## Actions

```
+----------------------+------+-----------------+---------------------------------+
| ref                  | pack | name            | description                     |
+----------------------+------+-----------------+---------------------------------+
| nest.get_humidity    | nest | get_humidity    | Get the current humidity        |
| nest.get_mode        | nest | get_mode        | Manage nest modes               |
| nest.get_temperature | nest | get_temperature | Get the current temperature.    |
| nest.set_away        | nest | set_away        | Set nest to away mode           |
| nest.set_fan         | nest | set_fan         | Manage fan state                |
| nest.set_home        | nest | set_home        | Set nest to home mode           |
| nest.set_humidity    | nest | set_humidity    | Set humidity goal for nest      |
| nest.set_mode        | nest | set_mode        | Set current operating mode      |
| nest.set_temperature | nest | set_temperature | Set current temperature.        |
| nest.show            | nest | show            | Show current Nest information   |
| nest.toggle_away     | nest | toggle_away     | Toggle current Home/Away status |
+----------------------+------+-----------------+---------------------------------+
```
