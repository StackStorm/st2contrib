#!/usr/bin/env python

import sys
import requests
import json
import os
import yaml

from getpass import getpass
from st2actions.runners.pythonrunner import Action

class ListScanExecutions(Action):
    def run(self, scan_id=None):
        """
        The template class for 

        Returns: An blank Dict.

        Raises:
           ValueError: On lack of key in config.
        """

        # Set up the results
        results = {}

        url = "https://{}/api/scan/v1/scans/{}".format(self.config['api_host'],scan_id)
        payload = None
        headers = { "Accept": "application/json" }

        try:
            r = requests.get(url,
                             headers=headers,
                             auth=(self.config['api_key'], ''))
            r.raise_for_status()
        except:
            raise ValueError("HTTP error: %s" % r.status_code)

        try:
            data = r.json()
        except:
            raise ValueError("Invalid JSON")
        else:
            return data
