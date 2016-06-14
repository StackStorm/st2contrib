# OpsGenie Pack

This integration pack allows you to intergrate with
[OpsGenie](https://www.opsgenie.com/). Which is a service to manage
alerts and oncall rotas.

You'll need an account and to create an integration API key and update
the packs `config.yaml`.

## Using OpsGenie for hubot Heartbeat

This requires 2 StackStorm installations, with both hubots in the same
channel.

The following needs to be configured in the datastore on both servers
(replace hubot with the other bot name):

```bash
st2 key set opsgenie_timer_hb_user "other_hubot"
st2 key set opsgenie_timer_hb_name "StackStorm ChatOps hubot"
st2 key set opsgenie_timer_hb_channel "chatops_heartbeat"
```

Then you need to add your Heartbeat to OpsGenie and test it:

```bash
st2 run opsgenie.add_heartbeat name="{{system.opsgenie_timer_hb_name}}" interval=30 enabled=true
st2 run opsgenie.send_heartbeat name="{{system.opsgenie_timer_hb_name}}"
```

If both of these are `successful` you can eanble them with:

```bash
st2 rule enable opsgenie.send_heartbeat_timer
```

To get an alert if it expires an intergration for Heartbeat should be
configured in the OpsGenie web interface.

## Configureation

Update the `config.yaml` to setup the API key for OpsGenie.

* `api_key` - The integration API key from the OpsGenie integration page.

## Coverage of OpsGenie API

Key: 
- [X] Completed.
- [-] Partial coverage.
- [?] Not currently planned.
- [ ] Outstanding for current version.  

[-] Alert API
    [-] Create Alert
    [X] Close Alert
    [X] Delete Alert
    [?] Get Alert
    [X] List Alerts
    [X] Count
    [?] List Alert Notes
    [?] Get Alert Activity Log
    [?] List Alert Recipients
    [?] Acknowledge
    [?] Snooze
    [?] Renotify
    [?] Take Ownership
    [?] Assign
    [?] Add Team
    [?] Add Recipient
    [?] Add Note
    [?] Add Tags
    [?] Remove Tags
    [?] Add Details
    [?] Remove Details
    [?] Execute Action
    [?] Attach File
[-] User API
    [?] Create User
    [?] Update User
    [?] Delete User
    [?] Get User
    [X] List Users
    [?] Copy Notification Rules To Other Users
[-] Group API
    [?] Create Group
    [?] Update Group
    [?] Add Member
    [?] Remove Member
    [?] Delete Group
    [?] Get Group
    [X] List Groups
[-] Team API
    [?] Create Team
    [?] Add Team Member
    [?] Remove Team Member
    [?] Update Team
    [?] Delete Team
    [?] Get Team
    [X] List Teams
    [?] List Team Logs
[?] Escalation API
    [?] Create Escalation
    [?] Update Escalation
    [?] Delete Escalation
    [?] Get Escalation
    [?] List Escalations
[-] Schedule API
    [?] Create Schedule
    [?] Update Schedule
    [?] Delete Schedule
    [?] Get Schedule
    [?] Get Schedule Timeline
    [?] List Schedules
    [?] Who is on-call
    [?] List Who is on-call
    [X] Who is on-call Next
    [?] Export Schedule
[?] Schedule Override API
    [?] Add Schedule Override
    [?] Update Schedule Override
    [?] Delete Schedule Override
    [?] Get Schedule Override
    [?] List Schedule Overrides
[?] Forwarding Rule API
    [?] Add Forwarding Rule
    [?] Update Forwarding Rule
    [?] Delete Forwarding Rule
    [?] Get Forwarding Rule
    [?] List Forwarding Rules
    [?] List Forwarding Rules for a User
[X] Heartbeat API
    [X] Add Heartbeat
    [X] Update Heartbeat
    [X] Enable Heartbeat
    [X] Disable Heartbeat
    [X] Delete Heartbeat
    [X] Get Heartbeat
    [X] List Heartbeats
    [X] Send Heartbeat
[?] Notification Rule API
    [?] Notification Rule API Requests
        [?] Add Notification Rule
	[?] Update Notification Rule
	[?] Delete Notification Rule
	[?] Enable Notification Rule
	[?] Disable Notification Rule
	[?] Change Notification Rule Order
	[?] Repeat Notification Rule
	[?] Get Notification Rule
	[?] List Notification Rules
	[?] Notification Rule Step API Requests
    [?] Add Notification Rule Step
        [?] Update Notification Rule Step
	[?] Delete Notification Rule Step
	[?] Enable Notification Rule Step
	[?] Disable Notification Rule Step
[?] Contacts API
    [?] Add Contact
    [?] Update Contact
    [?] Delete Contact
    [?] Enable Contact
    [?] Disable Contact
    [?] Get Contact
    [?] List Contact
[X] Integration API
    [X] Enable Integration
    [X] Disable Integration
[X] Policy API
    [X] Enable Policy
    [X] Disable Policy
[X] Account API
    [X] Get Account Info
