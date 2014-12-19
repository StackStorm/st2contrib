# Git Integration Pack

Pack which allows integration with Git repositories.

## Configuration

* ``url`` - URL to the Git repository you want to monitor. You can use any
  of supported transport protocols such as SSH or HTTP. For example:
  ``git@github.com:runseb/st2contrib.git`` (SSH transport),
  ``https://github.com/runseb/st2contrib.git`` (HTTP transport).

## Sensors

### GitCommitSensor

This sensors periodically polls defined Git repository for new commits. When a
new commit is detected, a trigger is dispatched.
