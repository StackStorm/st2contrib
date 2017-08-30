---
name: Sample
description: "Rule which sends an email when an email from johndoe@gmail.com is received"
pack: email
enabled: false
trigger:
  type: email.imap.message
  parameters: {}
criteria:
  trigger.from:
    pattern: johndoe@gmail.com
    type: contains
action:
  ref: core.sendmail
  parameters:
    body: 'We received an email'
    to: janedoe@gmail.com
    from: stackstorm@yourcompanyname.com
    subject: 'Email Received'
