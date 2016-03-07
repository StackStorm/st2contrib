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

def booleen2string(booleen):
    if booleen is True:
        return "true"
    else:
        return "false"
        
def GetScanResults (config, scan_exec_id, new_vulns=False, new_ports=False):
    """
    The template class for

    Returns: An blank Dict.

    Raises:
    ValueError: On lack of key in config.
    """

    results = {}
   
    url = "https://{}/api/scan/v1/results/{}".format(config['api_host'],scan_exec_id)

    payload = {}

    # The API expects false and not False, so send strings not booleens
    payload = { 'new_vulns': booleen2string(new_vulns),
                'new_ports': booleen2string(new_ports) }

    headers = { "Accept": "application/json" }

    try:
        r = requests.get(url,
                         headers=headers,
                         auth=(config['api_key'], ''),
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
