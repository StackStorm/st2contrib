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

        self._client = None
        self._repositories = []
        self._last_event_ids = {}

    def setup(self):
        self._client = Github(self._config['token'])

        for repository_dict in self._config['repository_sensor']['repositories']:
            user = self._client.get_user(repository_dict['user'])
            repository = user.get_repo(repository_dict['name'])
            self._repositories.append((repository_dict['name'], repository))

    def poll(self):
        for repository_name, repository_obj in self._repositories:
            self._logger.debug('Processing repository "%s"' %
                               (repository_name))
            self._process_repository(name=repository_name,
                                     repository=repository_obj)

    def _process_repository(self, name, repository):
        """
        Retrieve events for the provided repository and dispatch triggers for
        new events.

        :param name: Repository name.
        :type name: ``str``

        :param repository: Repository object.
        :type repository: :class:`Repository`
        """
        assert(isinstance(name, basestring))

        count = self._config['repository_sensor']['count']

        events = repository.get_events()[:count]
        events = list(reversed(list(events)))

        last_event_id = self._get_last_id(name=name)

        for event in events:
            if last_event_id and int(event.id) <= int(last_event_id):
                # This event has already been processed
                continue

            self._handle_event(repository=name, event=event)

        if events:
            self._set_last_id(name=name, last_id=events[-1].id)

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _get_last_id(self, name):
        """
        :param name: Repository name.
        :type name: ``str``
        """
        if not self._last_event_ids.get(name, None) and hasattr(self._sensor_service, 'get_value'):
            key_name = 'last_id.%s' % (name)
            self._last_event_ids[name] = self._sensor_service.get_value(name=key_name)

        return self._last_event_ids.get(name, None)

    def _set_last_id(self, name, last_id):
        """
        :param name: Repository name.
        :type name: ``str``
        """
        self._last_event_ids[name] = last_id

        if hasattr(self._sensor_service, 'set_value'):
            key_name = 'last_id.%s' % (name)
            self._sensor_service.set_value(name=key_name, value=last_id)

    def _handle_event(self, repository, event):
        if event.type not in self.EVENT_TYPE_WHITELIST:
            self._logger.debug('Skipping ignored event (type=%s)' % (event.type))
            return

        self._dispatch_trigger_for_event(repository=repository, event=event)

    def _dispatch_trigger_for_event(self, repository, event):
        trigger = self._trigger_ref

        created_at = event.created_at

        if created_at:
            created_at = created_at.strftime(DATE_FORMAT_STRING)

        # Common attributes
        payload = {
            'repository': repository,
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
