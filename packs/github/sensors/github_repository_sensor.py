import eventlet
from github import Github

from st2reactor.sensor.base import PollingSensor

eventlet.monkey_patch(
    os=True,
    select=True,
    socket=True,
    thread=True,
    time=True)

DATE_FORMAT_STRING = '%Y-%m-%d %H:%M:%S'


class GithubRepositorySensor(PollingSensor):
    EVENT_TYPE_WHITELIST = [
        'IssuesEvent',  # Triggered when an issue is assigned, unassigned, labeled, unlabeled,
                        # opened, closed, or reopened
        'IssueCommentEvent',  # Triggered when an issue comment is created
        'ForkEvent',  # Triggered when a user forks a repository,
        'WatchEvent'  # Triggered when a user stars a repository
    ]

    def __init__(self, sensor_service, config=None, poll_interval=None):
        super(GithubRepositorySensor, self).__init__(sensor_service=sensor_service,
                                                     config=config,
                                                     poll_interval=poll_interval)
        self._trigger_ref = 'github.repository_event'
        self._logger = self._sensor_service.get_logger(__name__)
        self._last_event_id = None

    def setup(self):
        self._client = Github(self._config['token'])

        self._user = self._client.get_user(self._config['repository_sensor']['user'])
        self._repository = self._user.get_repo(self._config['repository_sensor']['repository'])

    def poll(self):
        count = self._config['repository_sensor']['count']
        events = self._repository.get_events()[:count]
        events = list(reversed(list(events)))

        for event in events:
            if self._last_event_id and event.id <= self._last_event_id:
                # This event has already been processed
                continue

            self._handle_event(event=event)

        if events:
            self._last_event_id = events[-1].id

    def cleanup(self):
        # TODO: Persist last_id so we can resume
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _handle_event(self, event):
        if event.type not in self.EVENT_TYPE_WHITELIST:
            self._logger.debug('Skipping ignored event (type=%s)' % (event.type))
            return

        self._dispatch_trigger_for_event(event=event)

    def _dispatch_trigger_for_event(self, event):
        trigger = self._trigger_ref

        created_at = event.created_at

        if created_at:
            created_at = created_at.strftime(DATE_FORMAT_STRING)

        # Common attributes
        payload = {
            'id': event.id,
            'created_at': created_at,
            'type': event.type,
            'actor': {
                'id': event.actor.id,
                'login': event.actor.login,
                'name': event.actor.name,
                'email': event.actor.email,
                'loaction': event.actor.location,
                'bio': event.actor.bio,
                'url': event.actor.html_url
            },
            'payload': {}
        }

        event_specific_payload = self._get_payload_for_event(event=event)
        payload['payload'] = event_specific_payload
        self._sensor_service.dispatch(trigger=trigger, payload=payload)

    def _get_payload_for_event(self, event):
        payload = event.payload or {}
        return payload
