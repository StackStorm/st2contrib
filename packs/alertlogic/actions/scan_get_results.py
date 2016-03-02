#!/usr/bin/env python

import sys
import requests
import json
import os
import yaml

from getpass import getpass
from st2actions.runners.pythonrunner import Action

class GetScanResults(Action):
    def booleen2string(self, booleen):
        if booleen is True:
            return "true"
        else:
            return "false"

    def run(self, scan_exec_id=None, new_vulns=False, new_ports=False):
        """
        The template class for 

        Returns: An blank Dict.

        Raises:
           ValueError: On lack of key in config.
        """

        # Set up the results
        results = {}

        url = "https://{}/api/scan/v1/results/{}".format(self.config['api_host'],scan_exec_id)

        payload = {}
        
        # The API expects false and not False, so send strings not booleens
        payload = { 'new_vulns': self.booleen2string(new_vulns), 
                    'new_ports': self.booleen2string(new_ports) }

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
            return data
