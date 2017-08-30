from lib.base import BaseCubeSensorsAction


class GetDeviceAction(BaseCubeSensorsAction):
    def run(self, device_uid):
        response = self._perform_request('/devices/%s' % (device_uid))
        data = response.json()
        return data['device']
