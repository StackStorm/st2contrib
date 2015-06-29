# SmartThings IoT Integration Pack

This integration pack allows you to integrate with SmartThings. This works
by sending SmartThings events to StackStorm via HTTP Sensor.

The adapter is modeled heavily after [David Janes's SmartThings/MQTT](https://github.com/dpjanes/iotdb-smartthings)
and the [SmartTiles](http://www.smarttiles.click) to setup an API that can be
called via StackStorm actions located within this pack.

## Configuration

* `api_token` - API token to send commands from StackStorm -> SmartThings
* `api_endpoint` - HTTP endpoint for SmartThings SmartApp
* `api_key` - Shared API Key to send SmartThings events -> StackStorm

## Actions

* `disengage_lock`  - Disengage (lock) a device that can be locked
* `engage_lock`     - Engage (lock) a device that can be locked
* `find_id_by_name` - Lookup a specific device ID based on its name/type
* `get_device_info` - Get information on a specific device
* `list_devices`    - List devices of a specific type from SmartThings
* `set_mode`        - Set current temperature.
* `set_temperature` - Set current temperature.
* `toggle_lock`     - Toggle a lock
* `toggle_switch`   - Toggle a switch
* `turn_off_switch` - Turn off a light
* `turn_on_switch`  - Turn on a switch

## Installing SmartThings SmartApp

This integration requires a Groovy SmartApp installed in your SmartThings Developer acount. See
the file located at `etc/smartthings-adapter.groovy`.

* Log into SmartThings
  * https://graph.api.smartthings.com/
* Create a new SmartApp
  * Click on "+ New SmartApp"
  * Click on the "From Code" navigation element.
  * Copy and paste the contents of `etc/smartthings-adapter.groovy` into the empty dialog
  * Press "Create"
* Once the new SmartApp is created, Click "Publish" and select "For Me"
* In the right-hand pane, select your home location and press "Publish"
  * Once this refreshes, select the devices that you would like to be able to send/receive from
  * Ensure that the StackStorm FQDN and shared API key are set.
  * Press "Install"
* Finally, the Simulator should load. At the bottom of the right hand pane lies the `api_token` and `api_endpoint` values to be added to `config.yaml`
