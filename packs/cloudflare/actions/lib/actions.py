# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests

from st2actions.runners.pythonrunner import Action


class CloudflareBaseAction(Action):
    def __init__(self, config):
        super(CloudflareBaseAction, self).__init__(config)

        self.session = requests.Session()

        try:
            self.api_host = self.config['api_host']
        except KeyError:
            raise ValueError("Missing api host in the config.")

    def send_user_error(self, message):
        """
        Prints an user error message.
        """
        print(message)

    def _get(self, url, headers, payload):
        """
        Issue a get request via requests.session()

        Args:
            url: The URL.
            headers: The Headers
            payload: The Payload.

        Returns:
            dict: Of JSON payload.

        Raises:
            ValueError: On HTTP error or Invalid JSON.
        """

        try:
            r = self.session.get(url,
                                 headers=headers,
                                 params=payload)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            raise ValueError("HTTP error: %s" % r.status_code)

        try:
            data = r.json()
        except:
            raise ValueError("Invalid JSON")
        else:
            return data
