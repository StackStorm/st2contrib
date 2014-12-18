# Git Integration Pack

Pack which allows integration with Git repositories.

## Configuration

* ``url`` - URL to the Git repository you want to monitor (e.g.
  `git@demo-git:/home/git/repos/test.git`)

## Sensors

### GitCommitSensor

This sensors periodically polls defined Git repository for new commits. When a
new commit is detected, a trigger is dispatched.
