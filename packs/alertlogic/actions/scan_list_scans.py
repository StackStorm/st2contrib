#!/usr/bin/env python

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
