# PagerDuty 

This action enables the integration of PagerDuty into StackStorm. It is capable of performing the following actions:

1. List all the open incidents on PD for a subdomain
2. Send acknowledgment of any incident(s)
3. Close and open incident(s)
4. Launch an incident by giving its details and description

# Configuration

Copy the example configuration in [pagerduty.yaml.example](./pagerduty.yaml.example)
to `/opt/stackstorm/configs/pagerduty.yaml` and edit as required.

* `subdomain:` name of subdomain
* `api_key:` API-KEY
* `service_api:` SERVICE-API
* `debug:` optional debug flag. Set to True for additional logging

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Retrieving API Key from PagerDuty

* Sign into PagerDuty
* Head to `API Access` tab and navigate to the `New API` section
* Enter a description for the API key, and click `Create API Key`.
* Copy and paste the API key into `pagerduty.yaml`

## Retrieving Service Key from PagerDuty

* Sign into PagerDuty
* Head to the `Services` tab and click on `Add New Service`.
* Enter a name for the new service, and ensure the `Use our API directly` radio button is selected.
* Click `Add Service`.
* Copy and paste the service key into `pagerduty.yaml`
