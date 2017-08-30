# SignalR Integration Pack

Pack which allows triggers to be raised by SignalR

## Configuration

* ``hub_url`` - SignalR message hub URL
* ``hub_name`` -  The name of the hub for the sensor

## Actions
* `send_message` - Send a message to a hub

## Sensors

* `SignalRHubSensor` - Raises signalr.message_received triggers for messages on the hub
