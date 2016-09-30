# Datadog Integration Pack

This StackStorm Datadog integration pack supplies action integration for Datadog.

## Configuration

You will need to add your app and api keys to the config.yaml file:

```yaml
---
app_key: '9775a026f1ca7d1c6c5af9d94d9595a4'
api_key: '87ce4a24b5553d2e482ea8a8500e71b8ad4554ff'
 ```

You can generate the app and api key here: https://app.datadoghq.com/account/settings#api


## Actions

For further informations about the possible values of the actions and their syntax, see https://docs.datadoghq.com/api/


Name | Description
---- | -----------
checks.post_check_run | Post check run
comments.create_comment | Add a new comment
comments.delete_comment | Delete comment
comments.edit_comment | Edit comment
downtimes.schedule_monitor_downtime | Schedule monitor downtime
embeds.create_embed | Creates a new embeddable graph
embeds.enable_embed | Enable a specified embed
embeds.get_all_embeds | Gets a list of previously created embeddable graphs
embeds.get_embed | Get the HTML fragment for a previously generated embed with embed_id
embeds.revoke_embed | Revoke a specified embed
events.delete_event | Delete an event, not implemented
events.get_event | Query for event details
events.post_event | Post events to the stream
events.query_event | Query an event stream and filter by time, priority, sources or tags
graph.snapshot | Take graph snapshots
hosts.mute_host | Mute a host
hosts.unmute_host | Unmute a host
metrics.post_ts | Post time-series data that can be graphed on Datadog's dashboards
metrics.query_ts_points | Query for metrics from any time period
monitors.create_monitor | Create a monitor
monitors.delete_monitor | Delete an existing monitor
monitors.edit_monitor | Edit a monitor
monitors.get_all_monitors | Get all monitors
monitors.get_monitor | Get a monitor
monitors.mute_all_monitors | Muting will prevent all monitors from notifying through email and posts to the event stream. State changes will only be visible by checking the alert page.
monitors.mute_monitor | Mute a monitor
monitors.unmute_all_monitors | Disables muting all monitors
monitors.unmute_monitor | Unmute a monitor
screenboards.create_screenboard | Create a screenboard
screenboards.delete_screenboard | Delete an existing screenboard
screenboards.get_all_screenboards | Get all screenboards
screenboards.get_screenboard | Get a screenboard
screenboards.revoke_shared_screenboard | Revoke a currently shared screenboard
screenboards.share_screenboard | Share an existing screenboard with a public URL
screenboards.update_screenboard | Update a screenboard
search.search | Search for entities from the last 24 hours in Datadog
tags.add_host_tags | Add tags to a host on Datadog
tags.get_host_tags | Return the list of tags that apply to a given host
tags.get_tags | Return a mapping of tags to hosts for your whole infrastructure
tags.remove_host_tags | Remove all tags to a host on Datadog
tags.update_host_tags | Update all tags for a host on Datadog
timeboards.create_timeboard | Create a timeboard
timeboards.delete_timeboard | Delete an existing timeboard
timeboards.get_all_timeboards | Get all timeboards
timeboards.get_timeboard | Get a timeboard
timeboards.update_timeboard | Update a timeboard
users.create_user | Create a user on Datadog
users.disable_user | Disable user on Datadog
users.get_all_users | Get all users in your organisation from Datadog
users.get_user | Get informations for one your from Datadog
users.update_users | Update informations for a user from Datadog