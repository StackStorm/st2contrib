# Bitbucket Integration Pack

Pack for integration of Bitbucket into StackStorm. The pack includes the
functionality to perform actions on Bitbucket through StackStorm.

## Actions

### Repositories

#### List Repositories

This action is used to list all the repositories of a user.

Usage:

```bash
st2 run bitbucket.list_repos
```

#### Create Repository

This action is used to create a repository.

Usage:

```bash
st2 run bitbucket.create_repo repo="<repo-name-to-create>"
```

#### Delete Repository

This action is used to delete a repository.

Usage:

```bash
st2 run bitbucket.delete_repo repo="<repo-name-to-delete>"
```

#### Archiving a Repository

This action archives a repository and returns a path to the archived repository.

Usage:

```bash
st2 run bitbucket.archive_repo repo="<repo-name-to-archive>"
```

### Issues

#### Create Issue

This action is used to create an issue.

Usage:

```bash
st2 run bitbucket.create_issue repo="<repo-name>" title="<issue-title>" desc="<description-of-issue>" status=<new,open,resolved> kind="<bug, proposal>"
```

#### List Issues

This action is used to list all issues for a given repository.

Usage:

```bash
st2 run bitbucket.list_issues repo="<repo-name>"
```

#### Update Issues

This action is used to update issue's description for a given repository.

Usage:

```bash
st2 run bitbucket.update_issue repo="<repo-name>" id=<issue-id> desc="<updated-description>"
```

#### Delete Issues

This action is used to delete issues for a given repository. Provide an array of IDs (this can be
provided as a comma separated string of IDs using the CLI) to delete more than one issue.

Usage:

```bash
st2 run bitbucket.delete_issues repo="<repo-name>" ids=<1,2,3,4>
```

### Services

#### Create Service

This action to create a service/hook.

Usage:

```bash
st2 run bitbucket.create_service repo="<repo-name>" url="<URL-for-service>" service="<service-name-to-hook>"
```

#### List Services

This action is used to list services/hooks.

Usage:

```bash
st2 run bitbucket.list_services repo="<repo-name>"
```

#### Update Service

This action is used to update service/hook.

Usage:

```bash
st2 run bitbucket.update_service repo="<repo-name>" id=<id-of-service> url="<url-to-update>"
```

#### Delete Services

This action is used to delete services/hooks for a given repository.

Usage:

```bash
st2 run bitbucket.delete_services repo="<repo-name>" ids=<1,2,3,4>
```

### SSH Keys

#### List SSH keys

This action lists the SSH keys of a user.

Usage:

```bash
st2 run bitbucket.list_ssh_keys
```

#### Delete SSH key

This action deletes a SSH key associated with user's account.

Usage:

```bash
st2 run bitbucket.delete_ssh_key key_id=<id-of-ssh-key>
```

#### Associate SSH key

This action associates a SSH key associated with user's account.

Usage:

```bash
st2 run bitbucket.associate_ssh_key ssh_key="<ssh-key>" label="<label-for-SSH-key>"
```

### Branches

#### List Branches of a repository

This action lists the branches of a given repository.

Usage:

```bash
st2 run bitbucket.list_branches repo="<repo_name>"
```
<<<<<<< HEAD
=======

## Rules

### Post-Receive WebHook

This rule triggers ``packs.deploy`` action (in StackStorm v1.4+) to allow
auto-deployment of single pack repository.

This has a number of pre-dependancies:

- The repository being configured in:

```bash
/opt/stackstorm/packs/packs/config.yaml
```

- Setting an Workflow / Hooks / Post-Receive WebHooks pointing at the URL

```
https://<my-server>/api/v1/webhooks/bitbucket_post_receive?st2-api-key=<ST2-API-Key>
```

- The rule is disabled by default and needs to be enabled with

```bash
st2 rule enable bitbucket.post_receive_webhook
```

*Important:* The BitBucket server (or cloud) needs to be able to reach
your StackStorm server and consider the SSL cert as valid. The
`ST2-API-Key` should be generated as per the instructions at
https://docs.stackstorm.com/authentication.html.
>>>>>>> master
