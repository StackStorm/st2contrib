# Philips Hue Integration Pack

This integration pack allows you to integrate with
[Philips Hue](http://meethue.com) light bulbs.

This pack must be used on the same private network as the Hue bridge.

## Configuration

* `station_ip` IP address or FQDN of Philips Hue Bridge

## First Run

The first run of any action will block until it is authorized. After
installation, run the `hue.list_bulbs` and then press the button
on your Hue device to authorize StackStorm.

## Actions

Currently, the following actions listed below are supported:

```
+-----------------------+------+-------------------+------------------------------------------------------+
| ref                   | pack | name              | description                                          |
+-----------------------+------+-------------------+------------------------------------------------------+
| hue.alert             | hue  | alert             | Send an alert to a light                             |
| hue.brightness        | hue  | brightness        | Change the brightness of a bulb                      |
| hue.color_temp_kelvin | hue  | color_temp_kelvin | Change the bulb color temperature to a specific      |
|                       |      |                   | temperature in Kelvin                                |
| hue.color_temp_mired  | hue  | color_temp_mired  | Change the bulb color temperature to a specific      |
|                       |      |                   | temperature in mired scale                           |
| hue.current_state     | hue  | current_state     | Get current state of bridge                          |
| hue.find_id_by_name   | hue  | find_id_by_name   | Find bulb ID based on nickname                       |
| hue.list_bulbs        | hue  | list_bulbs        | List all registered bulbs                            |
| hue.off               | hue  | off               | Turn off a bulb                                      |
| hue.on                | hue  | on                | Turn on a bulb                                       |
| hue.rgb               | hue  | rgb               | Change bulb color based on RGB Values                |
| hue.set_state         | hue  | set_state         | Send manual state to bulb                            |
| hue.toggle            | hue  | toggle            | Toggle on/off state of a bulb                        |
| hue.xy                | hue  | xy                | Change bulb color based on CIE color space values    |
+-----------------------+------+-------------------+------------------------------------------------------+
```
