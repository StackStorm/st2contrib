from lib.actions import BaseAction

__all__ = [
    'GetObjectCDNURL'
]


class GetObjectCDNURL(BaseAction):
    api_type = 'storage'

    def run(self, credentials, container_name, object_name):
        driver = self._get_driver_for_credentials(credentials=credentials)

        obj = driver.get_object(container_name=container_name,
                                object_name=object_name)
        object_cdn_url = driver.get_object_cdn_url(obj=obj)

        result = {'url': object_cdn_url}
        return result
