#!/usr/bin/env python
# StackStorm

import requests
import time
import os
import uuid
import yaml
import sys

# Check_MK configuration

CMK_CONFIG_FILE = "/etc/check_mk/stackstorm.conf"
CMK_ENV_PREFIX = 'NOTIFY_'

# StackStorm configuration

ST2_API_BASE_URL = 'https://localhost/api/v1/'
ST2_TRIGGERTYPE_REF = 'check_mk.event_handler'
ST2_VERIFY_SSL = False


def main(config_file=CMK_CONFIG_FILE):
    config = read_config(config_file)
    st2_api_base_url = config.get('st2_api_base_url', ST2_API_BASE_URL)
    st2_trigger = config.get('st2_triggertype_ref', ST2_TRIGGERTYPE_REF)
    st2_verify_ssl = config.get('st2_verify_ssl', ST2_VERIFY_SSL)
    cmk_env_prefix = config.get('cmk_env_prefix', CMK_ENV_PREFIX)

    # gather all options from env
    context = dict([(key[len(cmk_env_prefix):], value.decode("utf-8"))
                    for (key, value) in os.environ.items()
                    if key.startswith(cmk_env_prefix)])

    trace_tag = uuid.uuid4()  # check_mk doesn't provide its own notification id
    payload = build_payload(context)
    headers = {
        'St2-Api-Key': config['api_key'],
        'St2-Trace-Tag': trace_tag
    }

    r = post_event_to_st2(st2_api_base_url, st2_trigger, payload, headers, verify=st2_verify_ssl)
    print "Sent event to StackStorm. HTTP_CODE: %d. TRACE_TAG: %s" % (r.status_code, trace_tag)


def read_config(config_file):
    try:
        with open(config_file) as f:
            config = yaml.safe_load(f)
    except IOError:
        print "Could not read file: %s" % config_file
        sys.exit(1)

    if "api_key" not in config:
        print "Required parameter %s missing from config file: %s" % ("api_key", config_file)
        sys.exit(2)

    return config


def build_payload(context):
    """
    Check_MK Contextual Data Example:
        CONTACTNAME=hirni
        CONTACTEMAIL=mk@hirni.de
        CONTACTPAGER=

        DATE=2012-11-08
        SHORTDATETIME=2012-11-08 14:07:1
        LONGDATETIME=Thu Nov 8 14:07:12 CET 2012

        NOTIFICATIONTYPE=PROBLEM
        LOGDIR=/omd/sites/hirn/var/check_mk/notify

        PARAMETERS=0199399485 Foo/Bar
        PARAMETER_1=0199399485
        PARAMETER_2=Foo/Bar

        HOSTNAME=localhost
        HOSTALIAS=localhost
        HOSTADDRESS=127.0.0.1
        HOSTCHECKCOMMAND=check-mk-ping
        HOSTNOTIFICATIONNUMBER=0
        HOSTOUTPUT=OK - 127.0.0.1: rta 0.054ms, lost 0%
        HOSTPERFDATA=rta=0.054ms;200.000;500.000;0; pl=0%;40;80;;
        HOSTSTATE=UP
        LASTHOSTSTATE=UP
        LONGHOSTOUTPUT=

        SERVICEDESC=fs_/
        SERVICECHECKCOMMAND=check_mk-df
        SERVICENOTIFICATIONNUMBER=7
        SERVICEOUTPUT=CRIT - 90.0% used (18.27 of 20.3 GB), (level
        SERVICEPERFDATA=/=18712.1132812MB;16630;18709;0;20788.5820
        SERVICESTATE=CRITICAL
        LASTSERVICESTATE=WARNING
        LONGSERVICEOUTPUT=
    """
    return {
        "notification_type": context.get("NOTIFICATIONTYPE"),
        "timestamp": to_epoch(context.get("SHORTDATETIME")),
        "parameters": context.get("PARAMETERS").split(),
        "contact": {
            "name": context.get("CONTACTNAME"),
            "email": context.get("CONTACTEMAIL"),
            "pager": context.get("CONTACTPAGER"),
        },
        "host": {
            "name": context.get("HOSTNAME"),
            "alias": context.get("HOSTALIAS"),
            "address": context.get("HOSTADDRESS"),
            "state": context.get("HOSTSTATE"),
            "last_state": context.get("LASTHOSTSTATE"),
            "output": context.get("HOSTOUTPUT"),
            "perf_data": context.get("HOSTPERFDATA"),
            "check_command": context.get("HOSTCHECKCOMMAND"),
            "notification_number": context.get("HOSTNOTIFICATIONNUMBER"),
            "long_output": context.get("LONGHOSTOUTPUT"),
        },
        "service": {
            "desc": context.get("SERVICEDESC"),
            "state": context.get("SERVICESTATE"),
            "last_state": context.get("LASTSERVICESTATE"),
            "output": context.get("SERVICEOUTPUT"),
            "perf_data": context.get("SERVICEPERFDATA"),
            "check_command": context.get("SERVICECHECKCOMMAND"),
            "notification_number": context.get("SERVICENOTIFICATIONNUMBER"),
            "long_output": context.get("LONGSERVICEOUTPUT"),
        }
    }


def to_epoch(cmk_ts):
    """Parse Check_MK's timestamp into epoch time"""
    return int(time.mktime(time.strptime(cmk_ts, '%Y-%m-%d %H:%M:%S')))


def post_event_to_st2(url, trigger, payload, headers, verify=False):
    body = {
        'trigger': trigger,
        'payload': payload
    }
    try:
        r = requests.post(url, json=body, headers=headers, verify=verify)
        r.raise_for_status()
        return r
    except requests.exceptions.RequestException as e:
        print "Error posting event to StackStorm: %s" % e
        sys.exit(3)


if __name__ == '__main__':
    main()
