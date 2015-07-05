# Travis CI Integration Pack

Pack for integration of Travis CI into StackStorm. The pack includes the
functionality to perform actions on Travis CI through StackStorm.

## Actions

### List Repos

The action to list all the repos for a supplied user, takes user name as an
argument to fetch its repositories.

Usage:

```bash
st2 run travisci.list_repos username=<user>
```

### List Builds

The action used to Get details like build id, commit id and branch name for a
given Repo. You need to provide reponame and username to get details.

Usage:

```bash
st2 run travisci.list_builds username="<username>" reponame="<reponame>"
```

### Start, Restart, Cancel Build

The action used to kick off / cancel a build against a build id. You can supply
any build id to kick-off/cancel a build for a speofic branch or a repo.

Usage:

```bash
st2 run travisci.start_build build_id=<build_id>
st2 run travisci.restart_build build_id=<build_id>
st2 run travisci.cancel_build build_id=<build_id>
```

### Retrieve list of branches for a repo

The action used to retrieve a list of branches for a particular repository.

Usage:

```bash
st2 run travisci.list_branches repo_id=<repo_id>
```

### List Hooks

The action used to Get hooks for a user's repositories. It returns all the
repositories enabled for Travis CI. It automatically includes Travis CI token
from the config file.

Usage:

```bash
st2 run travisci.list_hooks
```

### List Branches

The action used to Get branches for a given Repository

Usage:

```bash
st2 run travisci.list_branches repo_id=<repo_id>
```

### Enable, disable a hook

The action used to enable/disable hook for Travis CI tests. It requires one
argument - hook_id.

Usage:

```bash
st2 run travisci.enable_hook hook_id=<repo_id>
st2 run travisci.disable_hook hook_id=<repo_id>
```

## Configuration

Replace your Travis CI token in the config file and you are all set to use the
actions.

```yaml
token: Your Travis CI API access token
```

Note: Access token is not the token you find in your profile. For more
information, see [Authentication page](http://docs.travis-ci.com/api/#authentication).

### Getting Git Authentication Key

In order to get the git authentication with scopes, you need to go to settings
tab of your profile and then under settings tab go to `personal access token`.
Click on `Generate new token` and give it proper permissions read/write. Then
generate it. It will give you a key, you need to replace that in config file of
the pack.

![Alt text] (/_images/generate_new_token  "generate new token")


![Alt text] (/_images/permissions "Permissions to the token")
