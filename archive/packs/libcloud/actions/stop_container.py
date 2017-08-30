from lib.actions import BaseAction

__all__ = [
    'StopContainerAction'
]


class StopContainerAction(BaseAction):
    api_type = 'container'

    def run(self, credentials, container_id):
        driver = self._get_driver_for_credentials(credentials=credentials)
        container = driver.get_container(container_id)

        self.logger.info('Starting container: %s' % (container))
        status = container.stop()

        if status is True:
            self.logger.info(
                'Successfully stopped container "%s"' % (container))
        else:
            self.logger.error(
                'Failed to stopped container "%s"' % (container))

        return status
