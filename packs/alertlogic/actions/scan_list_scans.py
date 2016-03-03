#!/usr/bin/env python

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

import sys
import requests
import json
import os
import yaml

from getpass import getpass
from st2actions.runners.pythonrunner import Action

class ListScans(Action):
    def run(self, customer_id=None):
        """
        The template class for 

        Returns: An blank Dict.

        Raises:
           ValueError: On lack of key in config.
        """

        # Set up the results
        results = {}

        url = "https://{}/api/scan/v1/scans".format(self.config['api_host'])
        payload = None
        headers = { "Accept": "application/json" }

        if customer_id is not None:
            payload = {}
            payload['customer_id'] = customer_id

        try:
            r = requests.get(url,
                             headers=headers,
                             auth=(self.config['api_key'], ''),
                             params=payload)
            r.raise_for_status()
        except:
            raise ValueError("HTTP error: %s" % r.status_code)

        try:
            data = r.json()
        except:
            raise ValueError("Invalid JSON")
        else:
            for item in data:
                results[item['title']] = {"active": item["active"],
                                          "id": item["id"],
                                          "type": item["type" ] }
            return results
