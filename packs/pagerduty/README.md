# PagerDuty 

This action enables the integration of PagerDuty into StackStorm. It is capable of performing the following actions:

1. List all the open incidents on PD for a subdomain
2. Send acknowledgment of any incident(s)
3. Close and open incident(s)
4. Launch an incident by giving its details and description

# Configuration

`subdomain: `'name of subdomain '
`api_key:` API-KEY
`service_Api:` SERVICE-API

## Retrieving API Key from PagerDuty

* Sign into PagerDuty
* Head to `API Access` tab and navigate to the `New API` section
* Enter a description for the API key, and click `Create API Key`.
* Copy and paste the API key into `config.yaml`


## Retrieving Service Key from PagerDuty

* Sign into PagerDuty
* Head to the `Services` tab and click on `Add New Service`.
* Enter a name for the new service, and ensure the `Use our API directly` radio button is selected.
* Click `Add Service`.
* Copy and paste the service key into `config.yaml`

