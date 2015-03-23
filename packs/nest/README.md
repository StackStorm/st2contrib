# Nest Thermostat Integration Pack

This integration pack allows you to integrate with
[Nest](https://nest.com) thermostat.

## Configuration

* `username` - Nest.com username
* `password` - Nest.com password

## Actions

```
+------------------+------+-------------+------------------------------------------------------+
| ref              | pack | name        | description                                          |
+------------------+------+-------------+------------------------------------------------------+
| nest.fan         | nest | fan         | Manage fan state                                     |
| nest.humidity    | nest | humidity    | Manage humidity                                      |
| nest.mode        | nest | mode        | Manage nest modes                                    |
| nest.set_away    | nest | set_away    | Set nest to away mode                                |
| nest.set_home    | nest | set_home    | Set nest to home mode                                |
| nest.show        | nest | show        | Show current Nest information                        |
| nest.temperature | nest | temperature | Manage Nest temperature. Run with no attributes for  |
|                  |      |             | current state.                                       |
| nest.toggle_away | nest | toggle_away | Toggle current Home/Away status                      |
+------------------+------+-------------+------------------------------------------------------+
```
