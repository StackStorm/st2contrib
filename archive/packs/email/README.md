# EMail Integration Pack

This pack allows integration with EMail Services.

## Sensors
### SMTP Sensor

The SMTP Sensor runs a local server as defined in config.yaml, receiving email messages and emitting triggers into the system. This server is indiscriminate with what messages are received, and for whom. Basically, a catch-all for emails into the system.

As such, things like email filtering should happen upstream, or this should be run in a controlled environment.

```
# config.yaml
smtp_listen_ip: '127.0.0.1'
smtp_listen_port: 25
```

### IMAP Sensor

The IMAP Sensor logs into any number of IMAP servers as defined in config.yaml, polling for unread email messages and emitting triggers into the system. Sensor looks at one account and one folder at a time, and can be independently configured.

```
# config.yaml
imap_mailboxes:
  gmail_main:
    server: "gmail.imap.com"
    port: 993
    username: "james@stackstorm.com"
    password: "superawesomepassword"
    ssl: True
    download_attachments: False
  alternate:
    server: "mail.stackstorm.net"
    port: 143
    username: "stanley"
    password: "esteetew"
    folder: "StackStorm"
    ssl: True
    download_attachments: True
max_attachment_size: 1024
attachment_datastore_ttl: 1800
```

The following attachment settings can be configured:

* ``download_attachments`` - True to download the attachment and store them in the
  datastore.
* ``max_attachment_size`` - Maximum size of download attachment bytes. If an
  attachment exceeds this size the attachment won't be stored in the datastore.
* ``attachment_datastore_ttl`` - TTL in seconds for the attachment value which is
  stored in the datastore.

If ``download_attachments`` attribute for a particular IMAP server is set to ``True``,
attachments will be automatically downloaded and stored in the built-in datastore under
a unique key. This key will be available in the trigger payload (see the trigger example
bellow) so you can retrieve those attachments later (e.g. inside an action).

By default, those values have a TTL of 30 minutes which means they will be automatically remvoed
from the datastore after 30 minutes.

Keep in mind that all the attachments which contain binary (non plain-text, mime-type
!= text/plain) data are base64 encoded before they are stored in the datastore.

#### email.imap.message trigger

Example trigger payload:

```json
{
    "uid": 5780,
    "message_id": "<CAJMHEmJs_5hO_PS9huzTAOv60xkTvYz7ETd1=WXFdpa-bzGpUA@mail.gmail.com>",
    "from": "Tomaž Muraus<tomaz@tomaz.me>",
    "to": "Tomaz Muraus <tomaz.muraus@gmail.com>",
    "subject": "test email with attachment"
    "body": "hello from stackstorm!\n",
    "headers": [
        [
            "Delivered-To",
            "tomaz.muraus@gmail.com"
        ],
        [
            "Received",
            "by 10.182.33.5 with SMTP id n5csp2470866obi;        Wed, 10 Jun 2015 00:01:41 -0700 (PDT)"
        ],
        [
            "X-Received",
            "by 10.50.61.130 with SMTP id p2mr3867507igr.9.1433919701526;        Wed, 10 Jun 2015 00:01:41 -0700 (PDT)"
        ],
        [
            "Return-Path",
            "<kami@k5-storitve.net>"
        ],
        [
            "Received",
            "from mail-ig0-x230.google.com (mail-ig0-x230.google.com. [2607:f8b0:4001:c05::230])        by mx.google.com with ESMTPS id we7si8228902icb.8.2015.06.10.00.01.41        for <tomaz.muraus@gmail.com>        (version=TLSv1.2 cipher=ECDHE-RSA-AES128-GCM-SHA256 bits=128/128);        Wed, 10 Jun 2015 00:01:41 -0700 (PDT)"
        ],
        [
            "Received-Spf",
            "pass (google.com: domain of kami@k5-storitve.net designates 2607:f8b0:4001:c05::230 as permitted sender) client-ip=2607:f8b0:4001:c05::230;"
        ],
        [
            "Authentication-Results",
            "mx.google.com;       spf=pass (google.com: domain of kami@k5-storitve.net designates 2607:f8b0:4001:c05::230 as permitted sender) smtp.mail=kami@k5-storitve.net;       dkim=pass header.i=@tomaz.me"
        ],
        [
            "Received",
            "by mail-ig0-x230.google.com with SMTP id pi8so28796173igb.0        for <tomaz.muraus@gmail.com>; Wed, 10 Jun 2015 00:01:41 -0700 (PDT)"
        ],
        [
            "Dkim-Signature",
            "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=k5-storitve.net; s=google;        h=mime-version:sender:from:date:message-id:subject:to:content-type;        bh=dnyggWfMbPP+DPkMG3PmSW5Y7wvt84XbnBhbgnAUusg=;        b=VmO+M+kBxVU7BwCzreI3vza5kvkxUwkCsiZrlunnMfMnP60RJBJHhE3HtQmIITkjoD         v5fAou2vcSIm5eY/CYAbSJyzzhP6sNbVoHJl1Q90Gqb1KA8g3+hF+mBOBhIqEf0fKiRt         07f0maRrvwJdI54HHRuroE7jSs8DHNllWBJfY="
        ],
        [
            "Dkim-Signature",
            "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=tomaz.me; s=google;        h=mime-version:sender:from:date:message-id:subject:to:content-type;        bh=dnyggWfMbPP+DPkMG3PmSW5Y7wvt84XbnBhbgnAUusg=;        b=YQGGwcMru9HaWMTbcEtkDdALkSLwEANo/ruZ76REaeW8Hnj0U6aM+MLLRKLsiFwSM+         THzY92cpVDAlYkbDLyqN+PctHyOx3ofRobRjjv2741SzV8ZTYLPSyaqsLtOJlRbfo16m         U+9vVgux9/xGrGQnF4DckO86DlcDPPL4oPgBI="
        ],
        [
            "X-Google-Dkim-Signature",
            "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=1e100.net; s=20130820;        h=x-gm-message-state:mime-version:sender:from:date:message-id:subject         :to:content-type;        bh=dnyggWfMbPP+DPkMG3PmSW5Y7wvt84XbnBhbgnAUusg=;        b=TEvRNj86wdtz8SQWp1TfqIYOyFbVh6aEhVWcO1hXFf26fh6M36pRTty48qDzCN7dZb         hHZuKLTneCcgnhnt6bbVgR23AkeMtujFc2QGawF3e/So6Z8VGc1VMBoCdd3li0Epqj+w         OisxHlzV5HNhkcj+UB77345yGZBapcgoZxtn5/m6OaL+wDlWjLfgu0j0FHiMDlftJgF3         yMkgONFIZyVqz1xOey4rvjNBNpGowfF9ei0r869PzUjVLtYuw2UuvhXn0AbduxQHMxmA         1QY67srbOsz5DR+u0bX+2euzI7s5KDFCh1hredYctdr87lyEhJew6HYfCNYUXxxLF5R+         h8Wg=="
        ],
        [
            "X-Gm-Message-State",
            "ALoCoQmCaIs0LyyKWSiGNbUHv6N6osKVmVAuQ7zqUeNA+/7uh8fopFqq/hoF6Fry25ZELwjwbEPr"
        ],
        [
            "X-Received",
            "by 10.42.203.4 with SMTP id fg4mr3192769icb.52.1433919701095; Wed, 10 Jun 2015 00:01:41 -0700 (PDT)"
        ],
        [
            "Mime-Version",
            "1.0"
        ],
        [
            "Sender",
            "kami@k5-storitve.net"
        ],
        [
            "Received",
            "by 10.50.43.66 with HTTP; Wed, 10 Jun 2015 00:01:20 -0700 (PDT)"
        ],
        [
            "From",
            "Tomaž Muraus <tomaz@tomaz.me>"
        ],
        [
            "Date",
            "Wed, 10 Jun 2015 15:01:20 +0800"
        ],
        [
            "X-Google-Sender-Auth",
            "WfbOSpNXpbHPX2uAz0lP7j-8z7g"
        ],
        [
            "Message-Id",
            "<CAJMHEmJs_5hO_PS9huzTAOv60xkTvYz7ETd1=WXFdpa-bzGpUA@mail.gmail.com>"
        ],
        [
            "Subject",
            "test email with attachment"
        ],
        [
            "To",
            "Tomaz Muraus <tomaz.muraus@gmail.com>"
        ],
        [
            "Content-Type",
            [
                "multipart/mixed",
                {
                    "boundary": "20cf303f64066bc8ff0518247248"
                }
            ]
        ]
    ],
    "date": "Wed, 10 Jun 2015 15:01:20 +0800",
    "has_attachments": true,
    "attachments": [
        {
            "file_name": "hello stackstorm.txt",
            "datastore_key": "attachments-0d61eabdb749789c96853dcbbd933884",
            "content_type": "text/plain"
        }
    ],
    "mailbox_metadata": {
        "server": "email.stackstorm.com",
        "port": 993,
        "user": "kami@stackstorm.com",
        "folder": "Process",
        "ssl": true
    }
}
```
