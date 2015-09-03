# SaltStack Integration Pack

Pack which allows integration with SaltStack.

## Requirements

This pack depends on the salt Python library which requires the following
dependencies to be installed:

* SSL development headers and libraries (``libssl-dev`` package on Ubuntu)
* Swig (``swig`` package on Ubuntu)

Those requirements need to be installed on the server where the actions will
be running on and where you run ``packs.install``.

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

Saltstack runner/execution module function calls are represented as Stackstorm actions. Considering Saltstack's [`archive` execution module](http://docs.saltstack.com/en/2014.7/ref/modules/all/salt.modules.archive.html#module-salt.modules.archive), every function would be exposed as an Stackstorm action.

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

- local_archive.gzip
- local_archive.rar
- local_archive.tar
- local_archive.unrar
- local_archive.unzip
- local_archive.zip_
- local_cloud.action
- local_cloud.create
- local_cloud.destroy
- local_cloud.network_create
- local_cloud.profile_
- local_cloud.virtual_interface_create
- local_cloud.volume_attach
- local_cloud.volume_create
- local_cloud.volume_delete
- local_cloud.volume_detach
- local_cmdmod.run_chroot
- local_cmdmod.run
- local_cmdmod.script
- local_cp.get_file
- local_cp.get_url
- local_cp.push_dir
- local_cp.push
- local_cron.ls
- local_cron.rm_env
- local_cron.rm_job
- local_cron.set_env
- local_cron.set_job
- local_data.cas
- local_data.dump
- local_data.getval
- local_data.update
- local_event.fire_master
- local_event.fire
- local_event.send
- local_file.access
- local_file.chgrp
- local_file.chown
- local_file.directory_exists
- local_file.file_exists
- local_file.find
- local_file.manage_file
- local_file.mkdir
- local_file.remove
- local_file.replace
- local_file.search
- local_file.symlink
- local_file.touch
- local_file.truncate
- local_grains.append
- local_grains.delval
- local_grains.get
- local_grains.remove
- local_grains.setval
- local_hosts.add_hosts
- local_hosts.get_alias
- local_hosts.get_ip
- local_hosts.rm_host
- local_hosts.set_host
- local_htpasswd.useradd
- local_htpasswd.userdel
- local_mine.delete
- local_mine.get
- local_mine.send
- local_mine.update
- local_network.connect
- local_network.interface_ip
- local_network.ipaddrs
- local_network.ping
- local_network.subnets
- local_pillar.get
- local_pip.freeze
- local_pip.install
- local_pip.uninstall
- local_pkg.install
- local_pkg.refresh_db
- local_pkg.remove
- local_puppet.disable
- local_puppet.enable
- local_puppet.fact
- local_puppet.noop
- local_puppet.run
- local_puppet.status
- local_puppet.summary
- local_ret.get_fun
- local_ret.get_jids
- local_ret.get_jid
- local_ret.get_minions
- local_saltutil.sync_all
- local_saltutil.sync_grains
- local_saltutil.sync_modules
- local_saltutil.sync_outputters
- local_saltutil.sync_renderers
- local_saltutil.sync_returners
- local_saltutil.sync_states
- local_saltutil.sync_utils
- local_schedule.add
- local_schedule.delete
- local_schedule.disable_job
- local_schedule.enable_job
- local_schedule.run_job
- local_service.available
- local_service.restart
- local_service.start
- local_service.status
- local_service.stop
- local_shadow.del_password
- local_shadow.gen_password
- local_shadow.set_expire
- local_state.highstate
- local_state.single
- local_state.sls
- local_supervisord.add
- local_supervisord.custom
- local_supervisord.remove
- local_supervisord.reread
- local_supervisord.restart
- local_supervisord.start
- local_supervisord.stop
- local_systemd.available
- local_systemd.disable
- local_systemd.enable
- local_systemd.restart
- local_systemd.start
- local_systemd.stop
- local_systemd.systemctl_reload
- local_test.cross_test
- local_test.echo
- local_test.ping
- local_useradd.add
- local_useradd.chshell
- local_useradd.delete
