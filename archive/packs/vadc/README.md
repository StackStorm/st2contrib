# StackStorm vADC Pack

This pack is designed to manage vTMs via a Brocade Services Director. 

You can also manage individual vTMs directly, if you don't use Services
Director, but you will need to set brcd\_sd\_proxy to false and supply
appropriate brcd\_vtm\_\* config keys. See Configuration section below.

## Configuration File

You must create a configuration file:  `/opt/stackstorm/configs/vadc.yaml`

It should look like this:
```
---
  brcd_sd_proxy: true
  brcd_sd_host: "https://sd1.management.local:8100/"
  brcd_sd_user: "admin"
  brcd_sd_pass: "password"
  brcd_vtm_host: ""
  brcd_vtm_user: ""
  brcd_vtm_pass: ""
```

You only need to provide the brcd\_vtm\_\* values if you plan on calling
the vTMs directly.

The values can be static as above, or dynamic values as below: 
```
  brcd_sd_proxy: "{{system.brcd_sd_proxy}}"
  brcd_sd_host: "{{user.brcd_sd_host}}"
  brcd_sd_pass: "{{user.brcd_sd_pass}}"
```

**Note: You can't use "user" scoped keys with sensors**  
Sensors can only access system level keys. So if you want to use the
BSD Status Sensor below, then you'll need to use static keys or
Dynamic Keys in the system scope.  

See: https://github.com/StackStorm/st2/issues/2678

## Setting Dynamic Keys

Dynamic user values can be set with (for example):
```
    st2 key set --scope=user brcd_sd_host "https://sd1.brcd.local:8100/"
    st2 key set --scope=user brcd_sd_user "admin"
    st2 key set --scope=user brcd_sd_pass "password" --encrypt
```

## Sensors
### Brocade SD Status Sensor

This pack includes a sensor to monitor errors reported by the Services
Director.

The Sensor monitors your vTM status through the monitor/instance API.
Any errors which appear in the status of a vTM trigger alerts which can
then be processed by a rule.  

This sensor triggers vadc.bsd\_failure\_event

Enable the sensor with:
```
st2 sensor enable vadc.BrcdSdSensor
```

####Rules

*bsd\_chatops*  
If you have ChatOps enabled, then take a look at the rule and modify it
to suit your needs. Then enable the rule with:

```
st2 rule enable vadc.bsd_chatops
```

*vtm_fail_maintenance*  
This rule can be used to enable a "maintenance" TS automatically when
all nodes have failed in a pool. It gets triggered by the BSD Sensor
when the error\_level is error, and the failed\_nodes is not empty.

It only enabled the maintenance rule on vservers which use the failed
pool as their default.

Enable rule with:
```
st2 rule enable vadc.vtm_fail_maintenance
```

### Brocade Bandwidth Sensor

This sensor checks the current throughput of the vTMs registered in your
Services Director, and can alert you when they get close to their assigned
bandwidth or automatically assign bandwidth according to utilization.

Alerts will be generated when a VTM comes within 10 or `brcd\_bw\_warn` Mbps
of their currently assigned bandwidth.

If you set brcd\_bw\_manage to "all", or a CSV list of instances or tags,
then the sensor tracks those instances. The sensor tracks the last 10 or
`brcd\_bw\_track` throughput measurements, rounded up to the nearest 10 or
`brcd\_bw\_roundup` Mbps, and adds a headroom of 10 or `brcd\_bw\_headroom`
Mbps above this value.  

When vTMs get close to the assignment, an update event will be triggered,
which can be consumed by the `bsd\_bandwidth\_modify` rule.  

When in use, a minimum assigned bandwidth of (brcd\_bw\_minimum) Mbps will
be applied.  

To change the defaults, add the following static/dynamic keys to the pack
configuration file:
```
  brcd_bw_minimum: "{{system.brcd_bw_minimum}}"
  brcd_bw_headroom: "{{system.brcd_bw_headroom}}"
  brcd_bw_roundup: "{{system.brcd_bw_roundup}}"
  brcd_bw_track: "{{system.brcd_bw_track}}"
  brcd_bw_warn: "{{system.brcd_bw_vtm_warn}}"
  brcd_bw_manage: "{{system.brcd_bw_manage}}"
```

This sensor triggers vadc.bsd\_bandwidth\_event

Enable the sensor with:
```
st2 sensor enable vadc.BrcdBwSensor
```
####Rules

*bsd\_bandwidth_modify*
This rule takes the bsd\_bandwidth\_event trigger and updates the bandwidth
of the given vTM instance using the action: vadc.bsd\_set\_vtm\_bandwidth

*bsd\_bandwidth\_notify*
Posts the parameters from the vadc.bsd\_set\_vtm\_bandwidth event to a
chatops channel. Notifies of Bandwidth Change Trigger

*bsd\_bandwidth\_Alert*
Posts the parameters from the vadc.bsd\_set\_vtm\_bandwidth event to a
chatops channel. Notifies of Bandwidth Alert

Enable rules with:
```
st2 rule enable vadc.<rulename>
```


## Actions Included

Actions in the pack have required and optional paramaters. To get more
information about a specific action, you can use --help. For example:
```
st2 run vadc.bsd_list_vtms --help
```

The pack includes actions which manipulate or retrieve data from the
Services Director and also actions which configure the vTM itself. A
brief overview of the actions follow, but please use the --help system
for full details of an Action.  

_BSD Actions_

  * bsd\_get\_errors  
    Retrieve errors from the Services Director.  
    Returns a dictionary of failures  

  * bsd\_get\_status  
    retrieve status from the Services Director. You can optionally
    supply the instanceID/Tag of a specific vTM to get status of only
    that instance.  
    Returns a list of Status for all vTMs (or just one).  

  * bsd\_license\_vtm  
    Create an instance in the Services Director to license a vTM  
    You must provide vtm=<tag> and bw=<licensed bandwidth>  

  * bsd\ unlicense\_vtm  
    Mark a vTM instance as Deleted in the Services Director.  
    You must provide a vtm=<tag|ID> parameter.  

  * bsd\_list\_vtms   
    Retrieve the licensed vTMs from the Service Director. This returns
    a limited amount of information by default, but can provide more
    with full=true.

  * bsd\_get\_vtm\_bandwidth
    Retrieve the bandwidth assignments and usage from one or all
    of your vTMs. 

  * bsd\_set\_vtm\_bandwidth
    Set the bandwidth (bw) assigned to the given instance (vtm)
 
_vTM Actions_

All of these actions are designed to proxy through the Services
Director, so a vtm parameter is always required. However it isn't used
if brcd\_sd\_proxy is set to false.  

_Configuration_

  * vtm\_add\_pool  
    Create a pool on a vTM. You must provide the vtm, nodes, and name  

  * vtm\_add\_tip  
    Create a Traffic Ip Group on the vTM. You must provide the vtm,  
    name, a list of IP addresses, and a list of vTMs

  * vtm\_add\_vserver  
    Create a Virtual Server on the vTM. You must provide the vtm, name,
    pool, and TIP Group.  

  * There is also a delete action for all of the add actions above.  

_Operations_

  * vtm\_drain\_nodes  
    Mark a list of nodes as draining, or undrain the nodes in a pool.  
    You must provide the vtm, name, and a list of nodes. By default we
    drain nodes, but you can pass drain=false to undrain them.

  * vtm\_get\_pool\_nodes  
    Retrieve a list of nodes from the given pool. You must provide the
    vtm and the name of the pool.

  * vtm\_maintenance\_mode  
    Enabled or disable a Maintenance mode TrafficScript rule.  
    You must provide the vtm and vserver name, default is to enable the
    maintenance rule, and the default rule name is maintenance.

_Chains and workflows_

A couple of example workflows and chains are provided in the pack. They
both create and delete a service comprised of a pool, vserver and tip.

## Aliases Included

Aliases are used to present command aliases to ChatOps, a number are
included for ChatOps integration

__TODO__ List Aliases

