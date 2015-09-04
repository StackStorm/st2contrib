import time

from lib.sensors import OctopusDeploySensor


class NewDeploymentSensor(OctopusDeploySensor):
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
        super(NewDeploymentSensor, self).__init__(sensor_service=sensor_service,
                                                  config=config,
                                                  poll_interval=poll_interval)
        self._trigger_ref = 'octopusdeploy.new_deployment'
        self._logger = self._sensor_service.get_logger(__name__)
        self._deploy_key = 'octopusdeploy.last_deploy_date_str'
        self._last_date = None

    def setup(self):
        pass

    def poll(self):
        self._logger.debug('Requesting list of deployments')
        deployments = self._get_deployments()

        # Make sure there are releases
        if deployments is None:
            self._logger.info('No deployments found')
            return
        if len(deployments) is 0:
            self._logger.info('Empty list of deployments')
            return

        last_deployment = deployments[0]

        last_assembled_date = self._to_date(last_deployment['assembled'])

        # What is the last indexed release date? If none, index and exit
        index_date = self._get_last_date()
        self._logger.debug('Index date is %s' % index_date)
        if index_date is None:
            self._logger.info('Initializing index')
            self._set_last_date(last_assembled_date)
            index_date = self._get_last_date()

        # If there have been new deployments, trigger them each
        if last_assembled_date > index_date:
            self._logger.info('Found deployments to trigger')
            # Get deployments since the last update time
            # They are in date order so once you get one behind the index
            # break out of the loop
            for deployment in deployments:
                if self._to_date(deployment['assembled']) > index_date:
                    self._logger.info('Raising trigger for %s' % deployment['id'])
                    self._dispatch_trigger_for_deployment(deployment)
                else:
                    break
            self._set_last_date(last_assembled_date)
        else:
            self._logger.debug('No new deployments comparing %s'
                               % time.strftime("%Y-%m-%dT%H:%M:%S",
                                               last_assembled_date))
            self._logger.debug('and %s'
                               % time.strftime("%Y-%m-%dT%H:%M:%S",
                                               index_date))

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _get_deployments(self):
        result = self.make_get_request("deployments")
        releases = self._to_triggers(result['Items'])
        return releases

    def _to_date(self, date_string):
        date_string = date_string.split('.')[0]
        return time.strptime(date_string, '%Y-%m-%dT%H:%M:%S')

    def _get_last_deployment(self):
        deployments = self._get_deployments()
        if deployments is None:
            return None
        if len(deployments) is not 1:
            return None
        return deployments[0]

    def _get_last_date(self):
        self._last_date = self._sensor_service.get_value(name=self._deploy_key)
        if self._last_date is None:
            return None
        return time.strptime(self._last_date, '%Y-%m-%dT%H:%M:%S')

    def _set_last_date(self, last_date):
        self._last_date = time.strftime('%Y-%m-%dT%H:%M:%S', last_date)
        self._sensor_service.set_value(name=self._deploy_key,
                                       value=self._last_date)

    def _to_triggers(self, releases):
        triggers = []
        for release in releases:
            triggers.append(self._to_trigger(release))
        return triggers

    def _to_trigger(self, deployment):
        trigger = {
            'id': deployment['Id'],
            'name': deployment['Name'],
            'comments': deployment['Comments'],
            'assembled': deployment['Created'],
            'version': deployment['ReleaseId'],
            'author': deployment['LastModifiedBy'],
            'project_id': deployment['ProjectId']
        }
        return trigger

    def _dispatch_trigger_for_deployment(self, trigger_payload):
        trigger = self._trigger_ref
        self._sensor_service.dispatch(trigger=trigger, payload=trigger_payload)
