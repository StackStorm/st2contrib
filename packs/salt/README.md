# SaltStack Integration Pack

Pack which allows integration with SaltStack.

## Usage Options

### Scenario 1: ST2 Installed on a Salt Master

#### Configuration

This should be installed on the master

#### Examples

```bash
    st2 run salt.client matches='web*' module=test.ping
    st2 run salt.client module=pkg.install kwargs='{"pkgs":["git","httpd"]}'

    st2 run salt.bootstrap instance_id=<uuid> provider=my-nova name=web.example.com
```

### Scenario 2: ST2 Using Salt NetAPI

#### Configuration

In config.yaml:

```yaml
---
api_url: https://salt.example.com
username: stella
password: clams
```

#### Examples

```bash
    st2 run salt.runner_manage.up
    st2 run salt.runner_job.list_jobs kwargs='{"ext_source":"blah"}'
```

One can also use the generic "runner" action to execute arbitrary runners.

```bash
    st2 run salt.runner module=manage.down
```

