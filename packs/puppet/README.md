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

For the Python runner actions to work, you need to configure the following
items in the config:

* `master.hostname` - hostname of the puppet master
* `master.port` - port of the puppet master

* `auth.client_cert_path` - path to the client certificate file used for authentication
* `auth.client_cert_key_path` - path to the private key file for the client certificate
* `auth.ca_cert_path` - path to the CA cert file

Remote actions require no configuration. You simply need to specify server to
run the action on when running the action (same as with other remote actions).
