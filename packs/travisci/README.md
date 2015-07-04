# Travis CI Integration Pack

Pack for integration of Travis CI into StackStorm . The pack includes the
functionality to perform actions on TravisCI through StackStorm.

## Actions

### List Repos

The action to list all the repos for a supplied user, takes user name as an
argument to fetch its repositories.

Usage:

```bash
st2 run travisci.list_repos username=<user>
```

### Get Build Details

The action used to Get details like build id, commit id and branch name for a
given Repo. You need to provide reponame and username to get details.

Usage:

```bash
st2 run travisci.get_builds username="<username>" reponame="<reponame>"


### Start, Restart, Canel Build

The action used to kick off / cancel a build against a build id. You can supply
any build id to kick-off/cancel a build for a speofic branch or a repo.

Usage: st2 run travisci.start_build buildid = <build_id> action = "restart/cancel"

```bash
st2 run travisci.start_build buildid=<build_id>
st2 run travisci.restart_build buildid=<build_id>
st2 run travisci.cancel_build buildid=<build_id>
```

### Retrieve list of branches for a Repo

The action used to Get a list of branches for a particular repository.

```bash
st2 run travisci.get_branches repoid = "<repoid>"
```

### Get Hooks

The action used to Get hooks for a user's repositories. It returns all the
repositories enabled for Travis CI. It automatically includes Travis CI token
from the config file.

```bash
st2 run travisci.get_hooks
```

### Get Branches

The action used to Get branches for a given Repository

```bash
st2 run travisci.get_branches repo_id=<repo_id>
```

### Enable, disable

The action used to enable/disable hook for Travis CI tests. It requires one
argument - hookid.

```bash
st2 run travisci.enable_hook hookid=<repo_id>
st2 run travisci.disable_hook hookid=<repo_id>
```

## Configuration

Replace your git authentication key and Travis CI token in the config file and
you are all set to use the actions

```yaml
git_auth_key: Your Git Authentication Key
User-Agent: MyClient/1.0.0
Accept: application/vnd.travis-ci.2+json
Host: api.travis-ci.org
Authorization: token Your Travis CI token
Content-Type: application/json
uri: https://api.travis-ci.org
```

### Getting Git Authentication Key

In order to get the git authentication with scopes, you need to go to settings
tab of your profile and then under settings tab go to `personal access token`.
Click on `Generate new token` and give it proper permissions read/write. Then
generate it. It will give you a key, you need to replace that in config file of
the pack.

![Alt text] (/_images/generate_new_token  "generate new token")


![Alt text] (/_images/permissions "Permissions to the token")

### Getting Travis CI Token

When you make your profile on Travis CI you will be assigned a token for Travis
API. You can see that by clicking on you profile settings tab. Once you have
the token replace it in config file of action so it can communicate with the
Travis CI endpoints after authentication.

![Alt text] (/_images/travisci "Getting token from Travis CI")
