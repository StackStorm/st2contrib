from lib.actions import BaseAction

__all__ = [
    'DestroyContainerAction'
]


class DestroyContainerAction(BaseAction):
    api_type = 'container'

    def run(self, credentials, container_id):
        driver = self._get_driver_for_credentials(credentials=credentials)
        container = self.get_container(container_id)

        self.logger('Destroying container: %s...' % (container))
        status = driver.destroy_container(container)

        if status is True:
            self.logger.info('Successfully destroyed container "%s"' % (container))
        else:
            self.logger.error('Failed to destroy container "%s"' % (container))

        return status
