Setting up St2 to use rsyslog
============

####Introduction
Following these directions you can set up St2 to log via rsyslog either locally or remotely.

#### Setup St2 to use syslog

Configure st2 to use syslog.  In /etc/st2/st2.conf, make sure these lines to point to syslog.conf instead of logging.conf:

    logging = /etc/st2api/syslog.conf
    logging = /etc/st2reactor/syslog.conf
    logging = /etc/st2actions/syslog.conf
    logging = /etc/st2auth/syslog.conf

Restart St2:

    st2ctl restart

Next you can either configure the system to log via syslog on the local host, or point to a remote syslog server.

#### Setup local syslog

First configure rsyslog to accept messages via UDP on port 514.  Make sure these two lines in rsyslog.conf are uncommented:

    $ModLoad imudp
    $UDPServerRun 514

Next, copy the st2 syslog configuration file in place:

    cp 10-st2.syslog.conf /etc/rsyslog.d/

Then restart rsyslog:

    /etc/init.d/rsyslog restart

#### Remote syslog

To configure St2 to log to a remote server, change the host (and port if applicable) in /etc/st2/st2.conf:

    [syslog]
    host = localhost
    port = 514
    facility = local7

Restart St2:

    st2ctl restart

