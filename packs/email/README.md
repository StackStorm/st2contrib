# EMail Integration Pack

This pack allows integration with EMail Services.

## Sensors
### SMTP Sensor

The SMTP Sensor runs a local server as defined in config.txt, receiving email messages and emitting triggers into the system. This server is indiscriminate with what messages are received, and for whom. Basically, a catch-all for emails into the system.

As such, things like email filtering should happen upstream, or this should be run in a controlled environment.

```
# config.yaml
smtp_listen_ip: '127.0.0.1'
smtp_listen_port: 25
```

### IMAP Sensor

The IMAP Sensor logs into any number of IMAP servers as defined in config.txt, polling for unread email messages and emitting triggers into the system. Sensor looks at one account and one folder at a time, and can be independently configured.

```
# config.yaml
imap_mailboxes:
  gmail_main:
    server: "gmail.imap.com"
    port: 993
    username: "james@stackstorm.com"
    password: "superawesomepassword"
    ssl: True
  alternate:
    server: "mail.stackstorm.net"
    port: 143
    username: "stanley"
    password: "esteetew"
    folder: "StackStorm"
    ssl: True
```
