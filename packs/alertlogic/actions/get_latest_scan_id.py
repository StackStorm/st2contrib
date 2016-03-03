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

from scan_get_results import GetScanResults

class GetLatestScan(Action):
    def run(self, customer_id=None, scan_title=None):
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
            r.close()

        # get the scan ID...
        scans = {}
        for item in data:
            scans[item['title']] = {"active": item["active"], 
                                   "id": item["id"],
                                   "type": item["type" ] }

            
        url = "https://{}/api/scan/v1/scans/{}".format(self.config['api_host'],
                                                       scans[scan_title]['id'])
        payload = None
        headers = { "Accept": "application/json" }
                
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
            r.close()

        completed_scans = {}
        for item in data:
            if item['active'] is False:
                create_date = datetime.datetime.fromtimestamp(item['create_date']).strftime('%Y-%m-%d %H:%M:%S')
                finish_date = datetime.datetime.fromtimestamp(item['finish_date']).strftime('%Y-%m-%d %H:%M:%S')

                completed_scans[item['id']] = { "active":      item['active'],
                                                "create_date": create_date,
                                                "finish_date": finish_date
                                                }

        latest_scan_id = max(completed_scans.keys())

        #latest_scan = { 'scan_id': latest_scan_id,
        #                'create_date': completed_scans[latest_scan_id]["create_date"],
        #                'finish_date': results[latest_scan_id]["finish_date"]
        #            }
        #results[latest_scan_id] = completed_scans[latest_scan_id]

        ScanResults = GetScanResults(config)
        scan_results_raw = ScanResults.run(scan_exec_id=latest_scan_id, new_vulns=False, new_ports=False)

        ### Do the like Stuffs...

        scan_results = {}

        scan_results['details'] = {}
        scan_results['details']["customer_id"] = scan_results_raw["customer_id"]
        scan_results['details']["errors"] = scan_results_raw["errors"]

        scan_results['details']['scan'] = {}
        scan_results['details']['scan']['started'] = completed_scans[latest_scan_id]['create_date']
        scan_results['details']['scan']['finished'] = completed_scans[latest_scan_id]['finish_date']
        scan_results['details']['scan']['fast'] = scan_results_raw["fast_scan"]
        scan_results['details']['scan']['summary'] = scan_results_raw['scan_summary']

        scan_results['details']['totals'] = {}
        scan_results['details']['totals']['hosts'] = scan_results_raw["total_hosts"]
        scan_results['details']['totals']['vulns'] = scan_results_raw["total_vulns"]
        scan_results['details']['totals']['vulns_summary'] = scan_results_raw["vulns_summary"]

        scan_results['details']['policy'] = {}
        scan_results['details']['policy']['name'] = scan_results_raw["policy_name"]
        scan_results['details']['policy']['id'] = scan_results_raw["policy_id"]
        scan_results['details']['policy']['type'] = scan_results_raw["policy_type"]

        scan_results['hosts'] = {}
        for scanned_host in scan_results_raw['scanned_hosts']:
            scan_results['hosts'][ scanned_host['ip_address'] ] = {
                "host_name": scanned_host['host_name'],
                "tasks": scanned_host['tasks'],
                "ui_link": scanned_host['ui_link'],
                "vulnerable": None,
                "vulns_count": 0,
                "vulns": [],
            }

        for vh in scan_results_raw['vulnerable_hosts']:
            scan_results['hosts'][ vh['ip_address'] ]['vulnerable']  = True
            scan_results['hosts'][ vh['ip_address'] ]['vulns_count']  = len(vh['vulns'])

            scan_results['hosts'][ vh['ip_address'] ]['vulns'] = {  "Critical": [],
                                                                    "High": [],
                                                                    "Low": [],
                                                                    "Medium": [],
                                                                    "Unclassified": [],
                                                                    "Urgent": []
                                                                }
            ### This needs to be better...
            for vln in vh["vulns"]:
                scan_results['hosts'][ vh['ip_address'] ]['vulns'][ vln["risk_level"] ].append(vln)

            #scan_results['hosts'][ vh['ip_address'] ]['vulns'] = vh["vulns"]

        return scan_results
