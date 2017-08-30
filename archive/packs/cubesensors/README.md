# CubeSensors integration

Pack which allows integration with [CubeSensors](https://cubesensors.com/) service.

## Configuration

### General settings

* ``consumer_key`` - Your application consumer key.
* ``consumer_secret`` - Your application consumer secret.
* ``access_token`` - Access token retrieved during oAuth exchange.
* ``access_token_secret`` - Access token secret retrieved during oAuth exchange.

### Sensor settings

* ``sensor.device_uid`` - A list of device UIDs for which you want to retrieve the measurements
  for.

## Obtaining API credentials

To obtain the API credentials you first need to request API access as described
[here](https://cubesensors.com/faq/#data).

After API access has been granted, you should see new ``Your apps`` section on your account page
which lists consumer key and secret for your demo application.

You then need to use this information to perform the oAuth exchange and retrieve access token and
secret. For information on how to do that, please follow the
[instructions](https://my.cubesensors.com/docs) in the official API documentation.

## Sensors

### CubeSensorsMeasurementsSensor

This sensors polls [CubeSensors API](https://my.cubesensors.com/docs) for new measurements for each
device specified in the config and dispatches a trigger every time a new measurement is found.

By default, this sensor uses a poll interval of `90` seconds. Using a lower interval makes little
sense since the devices only retrieve measurements once a minute and the base station relays those
measurements to the cloud service every 1-2 minutes. This means a new measurement is only available
once every 1-2 minutes.

#### cubesensors.measurements trigger

Example trigger payload:

```json
{
    "device_uid": "000AAABBBCCCDDD",
    "device_name": "Bedroom",
    "measurements": {
        "noise": null,
        "cable": false,
        "temp": 22.78,
        "voc": 523,
        "battery": 98,
        "light": 6,
        "shake": false,
        "humidity": 41,
        "pressure": 976,
        "voc_resistance": 178475,
        "noisedba": 42,
        "time": "2015-08-14T12:36:00Z",
        "rssi": -59
    }
}
```

## Actions

* ``list_devices`` - List all the available devices (cubes).
* ``get_device`` - Retrieve information / details for a particular device (cube).
* ``get_measurements`` - Retrieve measurements for a particular device (cube).
