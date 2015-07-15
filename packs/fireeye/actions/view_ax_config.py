from lib.actions import BaseAction


class ViewAXConfig(BaseAction):
    def run(self):
        url = "/".join(self._url, 'config')
        r = requests.post(url=url, headers=self._headers)
        r.raise_for_status()
        return r.text
