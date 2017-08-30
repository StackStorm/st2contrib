from lib.action import BaseAction


class LookupDeviceAction(BaseAction):
    def run(self, name, device_type):
        url = "/{}".format(device_type)
        for device in self._get(url):
            if device['label'] == name:
                return device['id']
