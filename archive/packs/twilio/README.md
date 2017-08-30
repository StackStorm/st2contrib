# Twilio Integration Pack

Pack which allows integration with [Twilio](https://www.twilio.com/) service.

## Configuration

Copy the example configuration in [twilio.yaml.example](./twilio.yaml.example)
to `/opt/stackstorm/configs/twilio.yaml` and edit as required.

It must contain:

* ``account_sid`` - Your account sid (a 34 character string, starting with the
  letters AC).
* ``auth_token`` - Your authentication token.

Account sid and authentication token can be retrieved on the [Account
Dashboard][https://www.twilio.com/user/account/] page.

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Actions

* ``send_sms`` - Action which sends an SMS using Twilio API.
