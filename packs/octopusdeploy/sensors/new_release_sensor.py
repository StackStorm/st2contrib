import time

from lib.sensors import OctopusDeploySensor


class NewReleaseSensor(OctopusDeploySensor):
    """
    * self._sensor_service
        - provides utilities like
            get_logger() for writing to logs.
            dispatch() for dispatching triggers into the system.
    * self._config
        - contains configuration that was specified as
          config.yaml in the pack.
    * self._poll_interval
        - indicates the interval between two successive poll() calls.
    """

    def __init__(self, sensor_service, config=None, poll_interval=None):
        super(NewReleaseSensor, self).__init__(sensor_service=sensor_service,
                                               config=config,
                                               poll_interval=poll_interval)
        self._trigger_ref = 'octopusdeploy.new_release'
        self._logger = self._sensor_service.get_logger(__name__)
        self._release_key = 'last_release_date'
        self._last_date = None

    def setup(self):
        pass

    def poll(self):
        self._logger.debug('Requesting list of releases')
        releases = self._get_releases()

        # Make sure there are releases
        if releases is None:
            self._logger.debug('No releases found')
            return
        if len(releases) is 0:
            self._logger.debug('Empty list of releases')
            return

        last_release = releases[0]

        last_assembled_date = self._to_date(last_release['assembled'])

        # What is the last indexed release date? If none, index and exit
        index_date = self._get_last_date()
        if index_date is None:
            self._logger.debug('Initializing index')
            self._set_last_date(last_assembled_date)
            index_date = self._get_last_date()

        # If there have been new releases, trigger them each
        if last_assembled_date > index_date:
            self._logger.debug('Found releases to trigger')
            # Get releases since the last update time
            # They are in date order so once you get one behind the index
            # break out of the loop
            for release in releases:
                if self._to_date(release['assembled']) > index_date:
                    self._dispatch_trigger_for_release(release)
                else:
                    break
            self._set_last_date(index_date)

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _get_releases(self):
        result = self.make_get_request("releases")
        releases = self._to_triggers(result['Items'])
        return releases

    def _to_date(self, date_string):
        date_string = date_string.split('.')[0]
        return time.strptime(date_string, '%Y-%m-%dT%H:%M:%S')

    def _get_last_release(self):
        releases = self._get_releases()
        if releases is None:
            return None
        if len(releases) is not 1:
            return None
        return releases[0]

    def _get_last_date(self):
        if not self._last_date and hasattr(self._sensor_service, 'get_value'):
            self._last_date = self._sensor_service.get_value(name=self._release_key)

        return self._last_date

    def _set_last_date(self, last_date):
        self._last_date = last_date

        if hasattr(self._sensor_service, 'set_value'):
            self._sensor_service.set_value(name=self._release_key,
                                           value=last_date)

    def _to_triggers(self, releases):
        triggers = []
        for release in releases:
            triggers.append(self._to_trigger(release))
        return triggers

    def _to_trigger(self, release):
        trigger = {
            'id': release['Id'],
            'assembled': release['Assembled'],
            'release_notes': release['ReleaseNotes'],
            'version': release['Version'],
            'author': release['LastModifiedBy'],
            'project_id': release['ProjectId']
        }
        return trigger

    def _dispatch_trigger_for_release(self, trigger_payload):
        trigger = self._trigger_ref
        self._sensor_service.dispatch(trigger=trigger, payload=trigger_payload)
