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
import datetime

def GetScanExecutions(config, scan_id):
   """
   The template class for

   Returns: An blank Dict.
   
   Raises:
   ValueError: On lack of key in config.
   """
   
   results = {}

   url = "https://{}/api/scan/v1/scans/{}".format(config['api_host'], scan_id)
   payload = None
   headers = { "Accept": "application/json" }

   try:
      r = requests.get(url,
                       headers=headers,
                       auth=(config['api_key'], ''))
      r.raise_for_status()
   except:
      raise ValueError("HTTP error: %s on %s" % (r.status_code, r.url))

   try:
      data = r.json()
   except:
      raise ValueError("Invalid JSON")
   else:
      results = { 'latest_complete': None, 'scans': [] }
      for item in data:
         create_date = datetime.datetime.fromtimestamp(item['create_date'])
         finish_date = datetime.datetime.fromtimestamp(item['finish_date'])
         duration = finish_date - create_date

         results['scans'].append({ "id": item['id'],
                                   "active":      item['active'],
                                   "create_date": create_date.strftime('%Y-%m-%d %H:%M:%S'),
                                   "finish_date": finish_date.strftime('%Y-%m-%d %H:%M:%S'),
                                   "duration":    str(duration)
                                })
         
   # This list can be very large, limit to the last 10.
   results['scans'].sort(reverse=True)
   results['scans'] = results['scans'][0:10]

   # Find the latest ccmpleted scan..
   for item in results['scans']:
      if item['active'] is False:
         results['latest_complete'] = item['id']
         break

   return results

