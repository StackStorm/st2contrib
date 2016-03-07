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
import datetime

from getpass import getpass
from st2actions.runners.pythonrunner import Action

from lib.get_scan_list import GetScanList
from lib.get_scan_executions import GetScanExecutions
from lib.get_scan_results import GetScanResults

class GetScanResultsByTitle(Action):
    def run(self, customer_id=None, scan_title=None, new_vulns=False, new_ports=False):
        """
        The template class for 

        Returns: An blank Dict.

        Raises:
           ValueError: On lack of key in config.
        """

        scans = GetScanList(self.config, customer_id)
        scan_executions = GetScanExecutions(self.config,  scans[scan_title]['id'])

        latest_scan_id = scan_executions['latest_complete']

        return GetScanResults(self.config, latest_scan_id, new_vulns=new_vulns, new_ports=new_ports)
