from lib.actions import BaseAction

__all__ = [
    'GetContainerCDNURL'
]


class GetContainerCDNURL(BaseAction):
    api_type = 'storage'

    def run(self, credentials, container_name):
        driver = self._get_driver_for_credentials(credentials=credentials)

        container = driver.get_container(container_name=container_name)
        container_cdn_url = driver.get_container_cdn_url(container=container)

        result = {'url': container_cdn_url}
        return result
