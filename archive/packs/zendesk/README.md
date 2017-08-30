# Zendesk Integration Pack

This pack allows for Zendesk integrations.

## Configuration

Copy the example configuration in [zendesk.yaml.example](./zendesk.yaml.example)
to `/opt/stackstorm/configs/zendesk.yaml` and edit as required.

It must contain:

* ``email`` - Email of the account being used for the integration
* ``api_token`` - An API token generated in the admin interface
* ``subdomain`` - The subdomain of the zendesk account

To obtain a Zendesk API token, see the docs [here](https://developer.zendesk.com/rest_api/docs/core/introduction#api-token).

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Actions

* ``create_ticket`` - Creates a new ticket with the given subject and description.
* ``search_tickets`` - Searches all tickets for the given phrase.
* ``update_ticket`` - Updates the ticket with the given ID with a new comment.
* ``update_ticket_status`` - Updates the status of the ticket with the given ID.
