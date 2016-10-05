# Zendesk Integration Pack

This pack allows for Zendesk integrations.

## Configuration

* ``email`` - Email of the account being used for the integration
* ``api_token`` - An API token generated in the admin interface
* ``subdomain`` - The subdomain of the zendesk account

## Obtaining API Token

Zendesk's guide to getting access to API tokens can be found [here](https://developer.zendesk.com/rest_api/docs/core/introduction#api-token).

## Actions

* ``create_ticket`` - Creates a new ticket with the given subject and description.
* ``search_tickets`` - Searches all tickets for the given phrase.
* ``update_ticket`` - Updates the ticket with the given ID with a new comment.
* ``update_ticket_status`` - Updates the status of the ticket with the given ID.