# Jenkins Integration Pack

This pack creates a basic integration with Jenkins

To trigger events from Jenkins, use Jenkins to send a webhook to
StackStorm. Examples of rules can be found in the `rules` directory.

## Configuration

* `url` - FQDN to Jenkins API endpoint (e.x.: http://jenkins.mycompany.org:8080)
* `username` - Jenkins Username (if auth is enabled)
* `password` - Jenkins Password (if auth is enabled)

## Actions

* `build_job` - Kick off CI build based on project name
* `list_running_jobs` - List all currently running jobs
