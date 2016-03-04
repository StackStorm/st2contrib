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

from lib import GetScanList
from lib import GetScanExecutions

class ListScanExecutions(Action):
    def run(self, scan_title, customer_id=None):
        """
        The template class for 

        Returns: An blank Dict.

        Raises:
           ValueError: On lack of key in config.
        """

        # Set up the results
        results = {}

        # ChatOps is not passing None, so catch 0...
        if customer_id == 0:
            customer_id = None

        scans = GetScanList(self.config, customer_id)

        return GetScanExecutions(self.config, scans[scan_title]['id'])
