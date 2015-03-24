import json
from distutils.spawn import find_executable

import wmi_client_wrapper as wmi

from st2actions.runners.pythonrunner import Action

__all__ = [
    'WMIQueryAction'
]

WMIC_EXISTS = find_executable('wmic') is not None


class WMIQueryAction(Action):
    def run(self, host, password, query, username='Administrator'):
        if not WMIC_EXISTS:
            msg = ('Cannot find "wmic" binary. Please make sure WMI client (wmic) for'
                   ' Linux is installed and available in $PATH')
            raise Exception(msg)

        client = self._get_client(host=host, username=username,
                                  password=password)

        # Note: This method throws on connection issue, invalid query, etc
        result = client.query(query)

        try:
            result = json.dumps(result)
        except Exception:
            pass

        return result

    def _get_client(self, host, username, password):
        client = wmi.WmiClientWrapper(username=username,
                                      password=password,
                                      host=host)
        return client
