# <img src="http://www.ansible.com/favicon.ico" width="32px" valign="-3px"/> Ansible Integration Pack
This pack provides [Ansible](http://www.ansible.com/) integration to perform remote operations on both local and remote machines.
After [pack installation](http://docs.stackstorm.com/packs.html#getting-a-pack) all ansible executable files are available in pack virtualenv and ready to use.

## Actions
* `command` - Run single [Ad-Hoc command](http://docs.ansible.com/intro_adhoc.html). It has all the regular parameters of `ansible` executable.
* `command_local` - Perform single ansible Ad-Hoc command (module) locally.
* `playbook` - Action to run [Ansible Playbook](http://docs.ansible.com/playbooks.html) (`ansible-playbook` executable).
* `vault.encrypt` - Encrypt ansible data files (playbooks, vars, roles, etc) with password (`vault` executable).
* `vault.decrypt` - Decrypt ansible data files (playbooks, vars, roles, etc) with password (`vault` executable).
* `galaxy.install` - Install role from [Ansible Galaxy](http://docs.ansible.com/galaxy.html) - hub of [community developed roles](https://galaxy.ansible.com/) (`ansible-galaxy`).
* `galaxy.list` - List installed from Ansible Galaxy roles (`ansible-galaxy` executable).
* `galaxy.remove` - Remove the role installed from Ansible Galaxy (`ansible-galaxy` executable).

## Examples
See [StackStorm with Ansible on Vagrant demo](https://github.com/StackStorm/st2-ansible-vagrant) for more examples

#### `ansible.command` examples
```sh
# run ansible command with optional verbose parameter
st2 run ansible.command hosts=all args='hostname -i' verbose=vv
```

Action `ansible.command_local` is helper for the `ansible.command` with predefined parameters to run the command locally. So this is the same:
```sh
st2 run ansible.command_local args='echo $TERM'
st2 run ansible.command connection=local inventory-file='127.0.0.1,' hosts=all args='echo $TERM'
```
which is equivalent of ansible commands:
```sh
ansible all -c local -i '127.0.0.1,' -a 'echo $TERM'
ansible all --connection=local --inventory-file='127.0.0.1,' --args='echo $TERM'
```

#### `ansible.playbook` examples
```sh
# run some simple playbook
st2 run ansible.playbook playbook=/etc/ansible/playbooks/nginx.yml

# run playbook on last machine listed in inventory file 
st2 run ansible.playbook playbook=/etc/ansible/playbooks/nginx.yml limit='all[-1]'
```

#### `ansible.vault` examples
```sh
# encrypt /tmp/nginx.yml playbook with password containing in vault.txt
st2 run ansible.vault.encrypt vault-password-file=vault.txt files=/tmp/nginx.yml

# decrypt /etc/ansible/nginx.yml and /etc/ansible/db.yml files
st2 run ansible.vault.decrypt cwd=/etc/ansible vault-password-file=vault.txt files='nginx.yml db.yml'

# decrypt all files in /etc/ansible/playbooks directory
st2 run ansible.vault.decrypt cwd=/etc/ansible vault-password-file=vault.txt files='playbooks/*'
```

#### `ansible.galaxy` examples
```sh
# download many roles
st2 run ansible.galaxy.install roles='bennojoy.mysql kosssi.composer'

# list rolex
st2 run ansible.galaxy.list roles-path=/etc/ansible/roles
```
