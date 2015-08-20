# Packer Integration Pack

This integration pack allows StackStorm to control [Packer](http://packer.io),
a tool for creating machine and container images for multiple platforms
from a single source configuration.

Requires `packer` to be installed on Worker nodes. See _configuration_ for
additional details.

## Configuration

* `exec_path` - full path to packer binary (default: /usr/local/bin/packer)
* `atlas_token` - Hashicorp Atlas token, needed for `push` action.

## Actions
* `packer.build`    - Build images from a packer template
* `packer.fix`      - Takes a template and finds backwards
                      incompatible parts of it and brings it
                      up to date so it can be used with the
                      latest version of Packer
* `packer.inspect`  - Takes a template and outputs the
                      various components a template defines
* `packer.push`     - Push a template to Hashicorp Atlas
* `packer.validate` - Validate a packer template
