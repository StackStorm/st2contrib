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

import json
import requests

from st2actions.runners.pythonrunner import Action


class OpsGenieBaseAction(Action):
    def __init__(self, config):
        super(OpsGenieBaseAction, self).__init__(config)

        self.client = None
        self.session = requests.Session()

        try:
            self.api_key = self.config["api_key"]
            self.api_host = self.config["api_host"]
        except KeyError:
            raise ValueError("api_key and api_host needs to be configured!")

    def _url(self, uri):
        """
        """
        return "{}/{}".format(self.api_host.rstrip("/"),
                              uri)

    def _req(self, method, uri, payload=None, body=None):
        """
        """
        kwargs = {}

        if payload is None and body is None:
            raise ValueError("Need body or payload")

        if payload:
            kwargs["params"] = payload

        if body:
            kwargs['data'] = json.dumps(body)

        try:
            r = self.session.request(method,
                                     self._url(uri),
                                     **kwargs)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            raise ValueError("HTTP error: {}: '{}'".format(
                r.status_code, r.text))

        return r.json()
