from lib.base import BaseCubeSensorsAction


class ListDevicesAction(BaseCubeSensorsAction):
    def run(self):
        response = self._perform_request('/devices')
        data = response.json()
        return data['devices']
