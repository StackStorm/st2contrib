import os
import httplib

import requests

from lib.action import St2BaseAction

__all__ = [
    'UploadToS3'
]

S3_BUCKET_URL = 'https://%(bucket)s.s3.amazonaws.com/'


class UploadToS3(St2BaseAction):
    """
    Note: The destination bucket must be configured so everyone can write to it,
    but only we can read from it.
    """

    def run(self, bucket, file_name, remote_file=None):
        if not remote_file:
            remote_file = os.path.basename(file_name)

        if not os.path.isfile(file_name):
            raise ValueError('Local file "%s" doesn\'t exist' % (file_name))

        url = S3_BUCKET_URL % {'bucket': bucket}
        url = url + remote_file

        # Note: Requests library performs streaming and chunked upload
        files = {'file': open(file_name, 'rb')}
        response = requests.put(url=url, files=files)

        if response.status_code in [httplib.OK, httplib.CREATED]:
            status = 'ok'
            error = None
        else:
            status = 'failure'
            error = response.text

        result = {
            'status_code': response.status_code,
            'status': status,
            'uploaded_file': remote_file,
        }

        if error:
            result['error'] = error

        return result
