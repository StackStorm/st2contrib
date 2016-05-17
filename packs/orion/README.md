# Solarwinds Orion Integration Pack

This pack intergrates with Solarwinds Orion (a commerical monitoring
platform).

## Issues

- If don't have Orion NCM installed extra errors appear in the logs.

## Configuration

```yaml
orion:
  platform:
    host: orion-server
    user: stanley
    password: S0meth1ngSt0ng?
```

## StackStorm Version

This pack uses features released in 1.4+, if your using on an older
release some changes will be likley (at least removal of the `extra`
sections in some aliases and use of `use_none` in rules).

## Actions

tbc

## Rules

### Start Discovery Webhook

The JSON that should be posted to URL (XXXX) is as follows:

```json
{"orion_start_discovery": {
   "name": "My Example Discovery",
   "platform": "orion",
   "poller": "(primary|poller_name)",
   "snmp_communities": ["internal", "public"],
   "nodes": null | ["ip_address", "dns_name"],
   "subnets": null | ["10.1.0.0/255.0.0.0", "192.168.1.0/255.255.255.0" ]
   "ip_ranges": null | ["10.2.0.1:10.2.0.9", "192.168.2.1:"192.168.2.9"],
   "no_icmp_only": true | false,
   "auto_import": true | false
  }
}
```

The Discovery process in Orion, only supports a single choice out of
the following:

- nodes
- subnets
- ip_ranges

So only pick one or the action will fail.

It's most useful if auto_import is set to true, as currently no action
exists to call the `ImportDiscoveryResults` Verb. If it's set to
false, someone will need to visit the Orion WebUI and complete by
importing the discovery.

*Note:* The entires in the `snmp_communities` array can be standard
entires in the packs config.yaml or a community. However wither way
the community *must* already be in use in Orion and the
`Orion.Credential` table.
