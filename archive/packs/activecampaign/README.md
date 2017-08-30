# ActiveCampaign Integration pack

API: http://www.activecampaign.com/api/overview.php

To mass-produce actions, see `etc/ac_api_gen.py`

## Configuration

Copy the example configuration in [activecampaign.yaml.example](./activecampaign.yaml.example)
to `/opt/stackstorm/configs/activecampaign.yaml` and edit as required.

* ``url`` - ActiveCampaign account URL
* ``api_key`` - API Key

### Webhook Sensor Configuration

Webhook structure is http://host:port/path/action

* ``host`` - Defaults to "0.0.0.0"
* ``port`` - Defaults to 9991
* ``path`` - Defaults to "webhook"
