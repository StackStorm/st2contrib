This pack is designed to manage vTMs via a Brocade Services Director. 

You can also manage individual vTMs directly, if you don't use Services
Director, but you will need to set `brcd_sd_proxy` to false and supply
appropriate `brcd_vtm_*` config keys.

_Configuration File_

You must create a config yaml in:  /opt/stackstorm/configs/vadc.yaml 
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

You only need to provide the `brcd_vtm_` values if you plan on calling
the vTMs directly.

The values can be static as above, or dynamic values as below: 
```
  brcd_sd_proxy: "{{system.brcd_sd_proxy}}"
  brcd_sd_host: "{{user.brcd_sd_host}}"
  brcd_sd_pass: "{{user.brcd_sd_pass}}"
```

**Note: you can't use "user" scoped keys if you want to enable sensors,
because sensors can only access system level keys.**
See: https://github.com/StackStorm/st2/issues/2678

_Setting Dynamic Keys_

Dynamic user values can be set with (for example):
```
    st2 key set --scope=user brcd_sd_host "https://sd1.brcd.local:8100/"
    st2 key set --scope=user brcd_sd_user "admin"
    st2 key set --scope=user brcd_sd_pass "password" --encrypt
```

_BSD Status Sensor_

This pack includes a sensor to monitor errors reported by the Services
Director, and a rule which then reports those errors to ChatOps. 

If you have ChatOps enabled, then take a look at the rule and modify it
to suit your needs. Then enable the rule with:

```
st2 rule enable vadc.bsd_monitor
```

Alternatively you can edit rules/bsd_monitor.yaml and set:
```
  enabled: true
```

