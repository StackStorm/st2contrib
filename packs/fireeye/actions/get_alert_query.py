from lib.actions import BaseAction


class GetAlertQuery(BaseAction):
    def run(self, **kwargs):
        url = '/'.join([self._api_root, 'alerts'])
        r = requests.get(url=url, params=kwargs)
        r.raise_for_status()
        return r.to_json()
