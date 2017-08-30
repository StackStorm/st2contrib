# Vault Integration Pack

This pack is for Hashicorp Vault integrations

## Configuration

Copy the example configuration in [vault.yaml.example](./vault.yaml.example)
to `/opt/stackstorm/configs/vault.yaml` and edit as required.

It should contain:

* `url` - URL for the Vault server
* `cert` - Path to client-side certificate
* `token` - Authentication token
* `verify` - Whether to verify the SSL certificate or not

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Actions

* `delete` - Delete value from Vault server
* `get_policy` - Read policy from Vault server
* `is_initialized` - Read initialization status from Vault server
* `list_policies` - List policies from Vault server
* `read` - Read value from Vault server
* `write` - Write key/value to Vault server
