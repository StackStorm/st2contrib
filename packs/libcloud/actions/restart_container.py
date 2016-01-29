from lib.actions import BaseAction

__all__ = [
    'RestartContainerAction'
]


class RestartContainerAction(BaseAction):
    api_type = 'container'

    def run(self, credentials, container_id):
        driver = self._get_driver_for_credentials(credentials=credentials)
        container = driver.get_container(container_id)

        self.logger.info('Restarting container: %s' % (container))
        status = container.restart()

        if status is True:
            self.logger.info(
                'Successfully restarted container "%s"' % (container))
        else:
            self.logger.error(
                'Failed to restarted container "%s"' % (container))

        return status
