from lib.actions import BaseAction


class ViewAXConfig(BaseAction):
    def run(self):
        response = self._api_get('config')
        return response
