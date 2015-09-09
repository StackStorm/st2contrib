import requests

from st2actions.runners import pythonrunner


class GetWorkbookDefinitionAction(pythonrunner.Action):

    def run(self, workbook):
        url = self._get_api_url('workbooks', workbook)
        resp = requests.get(url)

        if resp.status_code != 200:
            raise Exception(resp.content)

        result = resp.json()

        if 'faultstring' in result:
            raise Exception(result.get('faultstring'))

        return result.get('definition')

    def _get_api_url(self, resource, resource_id):
        host = self.config['host']
        api_version = self.config['api_version']
        root = '%s%s' % (host, api_version)
        url = '%s/%s/%s' % (root, resource, resource_id)
        return url
