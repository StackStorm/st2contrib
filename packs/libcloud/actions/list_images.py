from lib.actions import BaseAction

__all__ = [
    'ListImagesAction'
]


class ListImagesAction(BaseAction):
    api_type = 'compute'

    def run(self, credentials):
        driver = self._get_driver_for_credentials(credentials=credentials)
        images = driver.list_images()
        return self.resultsets.formatter(images)
