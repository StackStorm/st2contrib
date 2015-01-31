# Chef integration pack

This pack integrates **StackStorm** with [**Chef**](https://www.chef.io/) and performs remote operations with chef nodes.

## Remote actions

Provide operations such as an installation of chef, invocation of *chef-solo/chef-client* as well as others. Remote actions require **hosts** parameter to be explicitly set.

### __chef.install action__

Performs an installation of chef on a remote node.

#### parameters:

`method` - Specify the method to install chef. (Omnibus is enabled by default, since it's the only supported way). *Default*: `'omnibus'`.

**Omnibus parameters:**

* `pre_release` - Set to `true` to install a pre-release version. Requires that version is also specified. *Default*: `false`.
* `version` - Specify a version of the chef-client to be installed. If no version is specified the latest version will be installed. *Default*: `none`.
* `download_path` - Use to specify the directory into which a omnibus package is downloaded. *Default*: `/tmp`.

### __chef.solo action__

Performs remote invocation of *chef-solo*.

#### parameters:

* `environment` - Specify a **string** to set the chef environment. *Default*: `none`.
* `attributes` - Specify a path on remote a node or URL to load json attributes from. *Default*: `none`. **Required**.
* `log_level` - Set the log level (debug, info, warn, error, fatal). *Default*: `none`.
* `why_run` - Set to `true` to enable whyrun mode. *Default*: `false`.
* `override_runlist` - Specify a **string** providing override run list. Replaces the current run list with specified items.
* `recipe_url` - Specify URL to pull down a remote gzipped tarball of recipes and untar it to the cookbook cache. *Default*: `none`.

### __chef.client action__

Performs remote invocation of *chef-client*.

#### parameters:

Use parameters *environment, attributes, log_level, why_run, override_runlist* which have the same meaning as for **chef.solo** action.

* `rewrite_runlist` - Specify a **string** providing rewrite run list. Permanently replaces the current run list with specified items. *Default*: `none`.
 
### __chef.ohai action__

Invokes ohai on remote nodes. The action accepts one single optional parameter which is a slash separated path to an ohai attribute.

### Examples
```shell
# Installing chef via omnibus
st2 run chef.install hosts=st2_agent_1 version=11.18.0 # to install the specified option
st2 run chef.install hosts=st2_agent_1 # to install latest version

# Invocation of chef-solo. /tmp/dna.json must present on remote nodes.
st2 run chef.solo hosts=st2_agent_1 recipe_url="https://github.com/dennybaa/st2-chef-test/raw/master/cookbooks.tgz" attributes=/tmp/dna.json 

# Querying ohai
st2 run chef.ohai hosts=st2_agent_1 network/interfaces/eth0/addresses
```
