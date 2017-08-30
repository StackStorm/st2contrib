# Duo Integration Pack

This pack intergrates with Duo (was Duo Secuirty), to allow 2FA to be
carried out within flows (everything expect sms is supported, but
defaults to auto).

## Auth Configuration 

You need an application intergration configured in the Duo interface
and the ikey, skey and host recorded in the `config.yaml`

```yaml
auth:
  host: api-hostname
  ikey: auth-api-integration-key
  skey: auth-api-secret-key
```

## Admin Configuration

To support feature actions, it's possible to configure an admin API
key, however this is not currently used.

```yaml
admin:
  host: api-hostname
  ikey: admin-api-integration-key
  skey: admin-api-secret-key
```

## Actions

### duo.auth_ping

Confirms if the configured host is up.

### duo.auth_check

Confirms if the configured host, ikey and skey are valid.

### duo.auth_auth

Carries out an authentication against Duo for the user (defaults to
`{{action_context.api_user}}`) and `auto` for the factor.

It's possible to use passcode if you collect the passcode from the
user in a secure manner.

Altho `sms` is a valid factor it's not included as it automaticly
denies the authentication and the user needs to be re-authed.