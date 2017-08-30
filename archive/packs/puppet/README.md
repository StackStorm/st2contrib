# Puppet Integration Pack

This intgeration pack allows for integration with [Puppet](http://puppetlabs.com/).

## Actions

Currently, the actions listed bellow are supported:

### Core

* Applying a standalone manifest to a local system - `apply`
* Run puppet agent - `run_agent`

### Certificate Management

* Certificate signing - `cert_sign`
* Certificate revocation - `cert_revoke`
* Certificate cleaning - `cert_clean`

## How it works

All the actions except `apply` and `agent_run` are Python runner
actions which are executed on the node where Stanley is running.

Those actions work by talking to the puppet master using the REST based HTTP
API.

`apply` and `agent_run` actions are remote runner actions. They
work by executing puppet CLI commands on the desired remote host.

#### Configuration

**BREAKING CHANGE**

The configuration in `config.yaml` has been flattened, and moved
to `config.schema.yaml`.

Any older configurationis (< v0.2.0) will need to be updated. `hostname` and `port`
are no longer subsections under `master` - they are now top-level
configuration items. Similarly, `client_cert_path`, `client_cert_key_path`,
`ca_cert_path` are now top-level items, not under `auth`.

Copy the example configuration in [puppet.yaml.example](./puppet.yaml.example)
to `/opt/stackstorm/configs/puppet.yaml` and edit as required.

* `hostname` - hostname of the puppet master
* `port` - port of the puppet master
* `client_cert_path` - path to the client certificate file used for authentication
* `client_cert_key_path` - path to the private key file for the client certificate
* `ca_cert_path` - path to the CA cert file

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

Remote actions require no configuration. You simply need to specify server to
run the action on when running the action (same as with other remote actions).
