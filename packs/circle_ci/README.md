# Circle CI Integration Pack

Pack for integration of Circle CI into StackStorm. The pack includes the
functionality to perform actions on Travis CI through StackStorm.

## Actions

### Get build number -  ```get_build_number```

The action to get the build number given a VCS revision and a project name.

Usage:

```bash
st2 run circle_ci.get_build_number project=<project> vcs_revision=<sha>
```

### Wait until build finishes - ```wait_until_build_finishes```

The action can be used to wait until a build finishes for a build number. An optional
```wait_timeout``` can be specified to specify the maximum wait time after which
the action fails if the build didn't complete.

Usage:

```bash
st2 run circle_ci.wait_until_build_finishes project=<project> build_number=<build> wait_timeout=<timeout>
```

### Get build info -  ```get_build_info```

The action to get the information of a build given a project name and build number.

Usage:

```bash
st2 run circle_ci.get_build_info project=<project> build_num=<build_num>
```

### Run build -  ```run_build```

The action to run a build given a project name and branch. Default branch name is `master`.

Usage:

```bash
st2 run circle_ci.run_build project=<project> branch=<branch_name>
OR
st2 run circle_ci.run_build project=<project> tag=<tag_name>
OR
st2 run circle_ci.run_build project=<project> vcs_revision=<sha>
```

### Retry build -  ```retry_build```

The action to retry a build given a project name and build number.

Usage:

```bash
st2 run circle_ci.retry_build project=<project> build_num=<build_num>
```

### Cancel build -  ```cancel_build```

The action to cancel a build given a project name and build number.

Usage:

```bash
st2 run circle_ci.cancel_build project=<project> build_num=<build_num>
```

## Configuration

Replace your Circle CI token in the config file and you are all set to use the
actions.

```yaml
token: Your Circle CI API access token
```
