## Mistral integration pack

### Configuration

Copy the example configuration in [mistral.yaml.example](./mistral.yaml.example)
to `/opt/stackstorm/configs/mistral.yaml` and edit as required.

It must contain:

* ``host`` - Mistral URL - e.g. 'http://localhost:8989/'
* ``api_version`` - Mistral API verson - e.g. 'v2'

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

### Actions

* get_task_results - Given an execution id, this action gets results for all the tasks for that execution.
* get_workflow_results - Given an execution id, this action gets the workflow status and the result of the entire workflow if one is available.
* kill_workflow - Kills a running mistral workflow.

