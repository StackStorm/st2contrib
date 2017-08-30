import httplib
from tempfile import NamedTemporaryFile

import requests
from six.moves import urllib

from st2actions.runners.pythonrunner import Action

CHUNK_SIZE = (512 * 1025)


class CaptureScreenshotAction(Action):
    def run(self, model, url, username=None, password=None, resolution=None):
        capture_url = self._get_capture_url(model=model, base_url=url, username=username,
                                            password=password, resolution=resolution)
        result = self._capture_screenshot(capture_url=capture_url)
        return result

    def _capture_screenshot(self, capture_url):
        print capture_url
        response = requests.get(capture_url)

        if response.status_code not in [httplib.OK, httplib.CREATED]:
            msg = 'Failed to capture screenshot: %s (%s)' % (response.text, response.status_code)
            raise Exception(msg)

        try:
            temp_file = NamedTemporaryFile(suffix='.jpg', delete=False)

            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    temp_file.write(chunk)
        finally:
            temp_file.close()

        return temp_file.name

    def _get_capture_url(self, model, base_url, username=None, password=None, resolution=None):
        """
        Return capture URL for a particular camera model.
        """
        query_params = {}

        if model == 'easyn':
            url = base_url + '/snapshot.jpg'
            if username:
                query_params['user'] = username
            if password:
                query_params['pwd'] = password
            if resolution:
                query_params['resolution'] = resolution
        else:
            raise ValueError('Unsupported model: %s' % (model))

        if query_params:
            url = url + '?' + urllib.parse.urlencode(query_params)

        return url
