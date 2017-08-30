from lib.actions import BaseAction


class GetAlertQuery(BaseAction):
    def run(self, **kwargs):
        response = self._api_get('/alerts', kwargs)
        return response
