from lib.actions import BaseAction


class ViewAXConfig(BaseAction):
    def run(self):
        url = "/".join([self._api_root, 'config'])
        r = requests.get(url=url, headers=self._headers)
        r.raise_for_status()
        return r.text
