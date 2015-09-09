from lib.action import BaseAction


class ListDevicesAction(BaseAction):
    def run(self, device_type):
        url = "/{}".format(device_type)
        return self._get(url)
