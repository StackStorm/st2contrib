# Cisco Spark Integration Pack

This integration pack allows you to integrate with
[Cisco Spark](http://www.ciscospark.com/),
the Enterprise Voice, instant messaging and collaboration platform by Cisco.

## Actions

Currently, the following actions listed bellow are supported:

### Message actions

* `send_message`
* `get_message`
* `list_messages`
* `delete_message`

### Room actions

* `create_room`
* `get_room`
* `update_room`
* `list_rooms`
* `delete_room`

### Team actions

* `create_team`
* `get_team`
* `update_team`
* `list_teams`
* `delete_team`

### Webhook actions

* `create_webhook`
* `get_webhook`
* `update_webhook`
* `list_webhooks`
* `delete_webhook`

## Configuration

Update config.yaml to setup the connection to Cisco Spark APIs.

* `access_token` - The API access token, can be fetched from developer.ciscospark.com
