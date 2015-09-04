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
        releases = self._get_releases()

        # Make sure there are releases
        if releases is None:
            return
        if len(releases) is 0:
            return

        last_release = releases[0]

        last_assembled_date = time.strptime(last_release.assembled)

        # What is the last indexed release date? If none, index and exit
        index_date_str = self._get_last_date()
        if index_date_str is None:
            self._set_last_date(last_release.assembled)
            return

        index_date = time.strptime(index_date_str)

        # If there have been new releases, trigger them each
        if last_assembled_date > index_date:
            # Get releases since the last update time
            # They are in date order so once you get one behind the index
            # break out of the loop
            for release in releases:
                if time.strptime(release.assembled) > index_date:
                    self._dispatch_trigger_for_release(release)
                else:
                    break
            self._set_last_date(index_date)

    def cleanup(self):
        pass

    def _get_releases(self):
        result = self.make_get_request("projects/releases")
        releases = self._to_triggers(result['Items'])
        return releases

    def _get_last_release(self):
        releases = self._get_releases()
        if releases is None:
            return None
        if len(releases) is not 1:
            return None
        return releases[0]

    def _get_last_date(self):
        if not self._last_id and hasattr(self._sensor_service, 'get_value'):
            self._last_id = self._sensor_service.get_value(name='last_id')

        return self._last_id

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
