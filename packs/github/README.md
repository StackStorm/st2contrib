# Github Integration Pack

Pack which allows integration with [Github](https://github.com/).

## Configuration

* ``token`` - Authentication token.
* ``repository_sensor.repositories`` - A list of repositories to monitor. Each
  item needs to contain the following keys: ``user`` - user or organization the
  repository you want to monitor belongs to and ``name`` - name of the
  repository you want to monitor.
* ``user`` - GitHub Username (only for use with ``get_traffic_stats`` and ``get_clone_stats`` actions).
* ``password`` - GitHub Password (only for use with ``get_traffic_stats`` and ``get_clone_stats`` actions).

## Obtaining Authentication Token

To obtain authentication token, follow the instructions on the [Creating an
access token for command-line use](https://help.github.com/articles/creating-an-access-token-for-command-line-use/)
page.

## Sensors

### GithubRepositorySensor

This sensor monitors Github repository for activity and dispatches a trigger
for each repository event.

Currently supported event types:

* ``IssuesEvent`` - Triggered when an issue is assigned, unassigned, labeled,
  unlabeled, closed, or reopened.
* ``IssueCommentEvent`` - Triggered when an issue comment is created.
* ``ForkEvent`` - Triggered when a user forks a repository.
* ``WatchEvent`` - Triggered when a user stars a repository.

#### github.repository_event trigger

Example trigger payload:

```json
{
    "repository": "st2",
    "id": "2482918921",
    "type": "WatchEvent",
    "created_at": "2014-12-25T11:47:27.000000Z",
    "actor": {
        "bio": null,
        "name": null,
        "url": "https://api.github.com/users/odyss009",
        "id": 483157,
        "loaction": null,
        "email": "redacted"
    },
    "payload": {
        "action": "started"
    }
}
```

All the events contain `repository`, `id`, `created_at`, `actor` and
`payload` attribute.

Value of the payload attribute depends on the event type. You can see a list
of the available event types and their attributes on the [Event Types &
Payloads](https://developer.github.com/v3/activity/events/types/) page.

Note: Similar thing can be achieved using Github webhooks in combination with
StackStorm webhook handler.

## Actions

* ``add_comment`` - Add comment to the provided issue / pull request.
* ``add_status`` - Add commit status to the provided commit.
