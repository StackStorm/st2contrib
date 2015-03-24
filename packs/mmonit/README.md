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