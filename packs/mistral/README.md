## Mistral integration pack

### Configuration

host - Mistral URL (For example, 'http://localhost:8989/')

api_version - Mistral API version (For example, 'v2')

### Actions

* get_task_results - Given an execution id, this action gets results for all the tasks for that execution.
* get_workflow_results - Given an execution id, this action gets the workflow status and the result of the entire workflow if one is available.
* kill_workflow - Kills a running mistral workflow.

