# Jenkins Integration Pack

This pack creates a basic integration with Jenkins

To trigger events from Jenkins, use Jenkins to send a webhook to StackStorm.
Examples of rules can be found in the `rules` directory.

Jenkins jobs are required to have the "parameterized" setting enabled in order
for this pack to be able to start jobs.

![param-step-1](https://cloud.githubusercontent.com/assets/125088/14975817/41cddcc8-10cb-11e6-8758-2c25e01d5227.png)

## Configuration

Copy the example configuration in [jenkins.yaml.example](./jenkins.yaml.example)
to `/opt/stackstorm/configs/jenkins.yaml` and edit as required.

* `url` - FQDN to Jenkins API endpoint (e.x.: http://jenkins.mycompany.org:8080)
* `username` - Jenkins Username (if auth is enabled)
* `password` - Jenkins Password (if auth is enabled)

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Actions

* `build_job` - Kick off CI build based on project name
* `list_running_jobs` - List all currently running jobs
* `enable_job` - Enable Jenkins job
* `disable_job` - Disable Jenkins job
* `get_job_info` - Retrieve Jenkins job information
* `install_plugin` - Install plugin
