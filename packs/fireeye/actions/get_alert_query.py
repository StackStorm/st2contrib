from lib.actions import BaseAction


class GetAlertQuery(BaseAction):
    def run(self, **kwargs):
        url = '/'.join(self._url, 'alerts')
        r = requests.post(url=url, params=kwargs, files=files)
        r.raise_for_status()
        return r.to_json()
