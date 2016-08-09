import fnmatch

import requests

from st2actions.runners.pythonrunner import Action

URL = 'https://%(api_token)s:@packagecloud.io/api/v1/repos/%(repo)s/packages.json'


class ListPackagesAction(Action):
    def run(self, repo, api_token, per_page=1000, filename_filter=None):
        values = {'repo': repo, 'api_token': api_token}
        url = URL % values
        params = {'per_page': per_page}

        response = requests.get(url, params=params)
        data = response.json()

        if not filename_filter:
            return data

        result = []
        for item in data:
            if fnmatch.fnmatch(item['filename'], filename_filter):
                result.append(item)

        return result
