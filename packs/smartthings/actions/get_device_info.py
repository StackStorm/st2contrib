from lib.action import BaseAction


class GetDeviceInfoAction(BaseAction):
    def run(self, device_type, device_id):
        url = "/{}{}".format(device_type, device_id)
        return self._get(url)
