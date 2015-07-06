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

### Actions

Saltstack runner/execution module function calls are represented as Stackstorm actions. Considering Saltstack's [`test` execution module](http://docs.saltstack.com/en/2014.7/ref/modules/all/salt.modules.archive.html#module-salt.modules.archive), every function would be exposed as an Stackstorm action.

Stackstorm actions for this pack are namespaced relative to their Saltstack NetAPI client name and module name. Thus having the form:

`[NetAPI client name]_[module name].[function name]`

An action named `runner_manage.down` calls the [`down` function from the `manage`](http://docs.saltstack.com/en/2014.7/ref/runners/all/salt.runners.manage.html#salt.runners.manage.down) runner.

#### Runner Actions

- runner_cache.clear_all
- runner_cache.clear_grains
- runner_cache.clear_mine_func
- runner_cache.clear_mine
- runner_cache.clear_pillar
- runner_cache.grains
- runner_cache.mine
- runner_cache.pillar
- runner_cloud.action
- runner_cloud.full_query
- runner_cloud.list_images
- runner_cloud.list_locations
- runner_cloud.list_sizes
- runner_cloud.profile
- runner_cloud.query
- runner_cloud.select_query
- runner_jobs.active
- runner_jobs.list_jobs
- runner_manage.down
- runner_manage.status
- runner_manage.up
- runner_manage.versions
- runner_pillar.show_pillar
- runner_pillar.show_top
- runner_thin.generate


#### Execution Module Actions
