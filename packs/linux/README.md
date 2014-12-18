# Linux Integration Pack

This pack contains actions for commonly used Linux commands and tools.

## Actions

* ``vmstat`` - Wrapper around the `vmstat` command.
* ``rsync`` - Wrapper around the `rsync` command.
* ``netstat`` - Wrapper around the `netstat` command.
* ``lsof`` - Wrapper around the `lsof` command.
* ``service`` - Action which allows you to perform an action (start, stop,
  restart, etc.) on a system service. Currently it supports the following
  distributions: Ubuntu / Debian (upstart, sys init), RedHat / Fedora
  (systemd).
* ``touch`` - Action which touches a file.

* ``check_loadavg`` - Action which retrieves load average from a remote host.
* ``check_processes`` - Action which retrieves useful information about
  matching process on a remote host.
