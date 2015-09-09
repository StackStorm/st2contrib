# Bitbucket Integration Pack

Pack for integration of Bitbucket into StackStorm. The pack includes the
functionality to perform actions on Bitbucket through StackStorm.

##Steps for using the pack

## Actions

### Repositories
#### List Repositories

This action is used to list all the repositories of a user

Usage:

```bash
st2 run bitbucket.list_repos
```

#### Create Repository

The action to create a repository

Usage:

```bash
st2 run bitbucket.create_repo repo="<repo-name-to-create>"
```

#### Delete Repository

The action to delete a repository

Usage:

```bash
st2 run bitbucket.delete_repo repo="<repo-name-to-delete>"
```

#### Archiving a Repository
The action to return a path to the archived repository

Usage:

```bash
st2 run bitbucket.archive_repo repo="<repo-name-to-archive>"
```

### Issues
#### Create Issue

The action to create a issue

Usage:

```bash
st2 run bitbucket.create_issue repo="<repo-name>" title="<issue-title>" desc="<description-of-issue>" status=<new,open,resolved> kind="<bug, proposal>"
```

#### List Issues

The action to List all issues for a given repository

Usage:

```bash
st2 run bitbucket.list_issues repo="<repo-name>"
```

#### Update Issues

The action to Update issue's description for a given repository

Usage:

```bash 
st2 run bitbucket.update_issue repo="<repo-name>" id=<issue-id> desc="<updated-description>"
```


#### Delete Issues

The action to Delete issues for a given repository. Provide comma seperated id's to delete more than one issue

Usage:

```bash 
st2 run bitbucket.delete_issues repo="<repo-name>" ids=<1,2,3,4>
```

### Services

#### Create Service

The action to create service/hook.

Usage:

```bash
st2 run bitbucket.create_service repo="<repo-name>" url="<URL-for-service>" service="<service-name-to-hook>"
```

#### List Services

The action to list services/hooks.

Usage:

```bash
st2 run bitbucket.list_services repo="<repo-name>"
```

#### Update Service

The action to update service/hook.

Usage:

```bash
st2 run bitbucket.update_service repo="<repo-name>" id=<id-of-service> url="<url-to-update>"
```

#### Delete Services

The action to Delete services/hooks for a given repository. Provide comma seperated id's to delete more than one service

Usage:

```bash 
st2 run bitbucket.delete_services repo="<repo-name>" ids=<1,2,3,4>
```

### SSH Keys

#### List SSH keys

This action lists the SSH keys of a user

Usage:

```bash 
st2 run bitbucket.list_ssh_keys
```

#### Delete SSH key

This action deletes a SSH key associated with user's account

Usage:

```bash
st2 run bitbucket.delete_ssh_key key_id=<id-of-ssh-key>
```

#### Associate SSH key

This action associates a SSH key associated with user's account

Usage:

```bash
st2 run bitbucket.associate_ssh_key ssh_key="<ssh-key>" label="<label-for-SSH-key>"
```

###Branches
#### List Branches of a repository

This action lists the branches of a given repository

Usage:

```bash 
st2 run bitbucket.list_branches repo="<repo_name>"
```
