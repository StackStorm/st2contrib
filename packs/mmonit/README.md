# Mmonit Integration Pack

Pack which allows integration with [Mmonit](http://www.mmonit.com/).

## Sensors

* ``new_event`` - Sensor that triggers a mmonit.new_event for any new events and sends the following payload:
``
  host:
    type: "string"
  id:
    type: "integer"
  event:
    type: "string"
  servicename:
    type: "string"
  full_data:
    type: "object"
``

## Sensors Config

* ``host`` - mmonit host to connect to.
* ``username`` - Username to connect to mmonit.
* ``password`` - Password to connect to mmonit.
* ``event_types`` - Comma separated list of events to listen for. Possible values: 0=success, 1=error, 2=change. 1 and 2 by default.
* ``active`` - The active events filter. Possible values: 0=show all events, 1=show only active errors, 2=show only active errors but exclude user dismissed errors. Defaults to 1.


## Actions

* ``list_status_hosts`` - Returns the current status of all hosts registered in M/Monit.
* ``get_status_host`` - Returns detailed status of the given host.
* ``summary_status`` - Returns a status summary of all hosts.
* ``list_uptime_hosts`` - Returns hosts uptime overview. If a custom range is used, the difference between datefrom and dateto should be in minutes, not in seconds since 1 minute is the lowest data resolution in M/Monit.
* ``get_uptime_host`` - Returns services uptime for a particular host.
* ``list_events`` - Returns a list of events stored in M/Monit. Arguments can be combined to select specific events.
* ``get_event`` - Returns details for a specific event.
* ``summary_events`` - Returns the events summary for the last 24 hours.
* ``dismiss_event`` - Dismiss the given active event so it doesn't show up in the event list if active filter is set to 2.
* ``list_hosts`` - Returns a list of all hosts registered in M/Monit.
* ``get_host`` - Returns details for the given host id.
* ``update_host`` - Updates the host settings in the M/Monit database.
* ``delete_host`` - Deletes the host with the given id.
* ``test_connection_to_host`` - Checks that M/Monit can connect to the host with the given network settings.
* ``action_host`` - Performs the specified action for the selected host services.
* ``session_put`` - Add or update the session attribute identified by key. If a named attribute already exist, its old value is replaced.
* ``session_get`` - Returns the session attribute matching the key argument. If no keys are specified, all stored attributes in the session are returned.
* ``session_delete`` - Returns the session attribute matching the key argument. If no keys are specified, all stored attributes in the session are returned.



## Actions Config

* ``host`` - mmonit host to connect to.
* ``username`` - Username to connect to mmonit.
* ``password`` - Password to connect to mmonit.