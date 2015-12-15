# Changelog

## v0.2

* Breaking Change: Replaced all dashes in parameter names with underscores (adhere to the spec of Jinja/Python variables)

## v0.1.1

* Prepend sandboxed path with ansible binaries to PATH env variable, allowing ansible binary discovery to follow PATH order

## v0.1.0

* Initial release with actions included:
 * `ansible.playbook`
 * `ansible.command`
 * `ansible.command_local`
 * `ansible.galaxy.install`
 * `ansible.galaxy.list`
 * `ansible.galaxy.remove`
 * `ansible.vault.encrypt`
 * `ansible.vault.decrypt`
