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
import copy
from st2actions.runners.pythonrunner import Action


class ICSPBaseActions(Action):

    def __init__(self, config):
        super(ICSPBaseActions, self).__init__(config)
        self.icsp_host = config['host']
        self.icsp_user = config['user']
        self.icsp_pass = config['pass']
        self.icsp_apiv = config['apiv']
        self.icsp_sslverify = config['sslverify']

    def check_results(self, results):
        # Check for errorCode json element
        if 'errorCode' in results:
            raise Exception("Error: %s" % (results["recommendedActions"]))

    def set_connection(self, connection=None):
        if connection:
            if 'host' in connection:
                self.icsp_host = connection['host']
            if 'user' in connection:
                self.icsp_user = connection['user']
            if 'pass' in connection:
                self.icsp_pass = connection['pass']
            if 'apiv' in connection:
                self.icsp_apiv = connection['apiv']
            if 'sslverify' in connection:
                if connection['sslverify'].lower() == "false":
                    self.icsp_sslverify = False
                else:
                    self.icsp_sslverify = True

    def get_sessionid(self):
        url = 'https://%s/rest/login-sessions' % self.icsp_host
        payload = {'userName': self.icsp_user, 'password': self.icsp_pass}
        headers = {'accept': 'application/json',
                   'accept-language': 'en-us',
                   'Content-Type': 'application/json'}
        p = requests.post(url, headers=headers,
                          json=payload, verify=self.icsp_sslverify)
        results = p.json()
        self.check_results(results)
        self.icsp_sessionid = results["sessionID"]

        # added here due to the requirement of the session id
        self.base_headers = {'Auth': str(self.icsp_sessionid),
                             'X-Api-Version': str(self.icsp_apiv)}

        return results["sessionID"]

    def extract_id(self, joburi):
        jobid = str(joburi)
        return int(jobid.split("/")[-1])

    def get_mids(self, ids, idtype):
        endpoint = "/rest/os-deployment-servers"
        getresults = self.icsp_get(endpoint)
        servers = getresults["members"]
        mids = []
        # id then server loop to ensure results match
        # the ID order not the icsp server order
        for id in ids:
            for server in servers:
                if (((idtype == 'serialnumber' and
                    server["serialNumber"] == id) or
                        (idtype == 'uuid' and
                            server["uuid"] == id)) and
                        server["mid"] not in mids):
                                mids.append(int(server["mid"]))
        return mids

    def validate_mids(self, identifiers):
        for n in identifiers:
            try:
                int(n)
            except:
                raise ValueError("Identifier provided is not a MID")

    def icsp_get(self, endpoint):
        url = 'https://%s%s' % (self.icsp_host, endpoint)
        headers = copy.copy(self.base_headers)
        p = requests.get(url, headers=headers, verify=self.icsp_sslverify)
        results = p.json()
        self.check_results(results)
        return results

    def icsp_put(self, endpoint, payload):
        url = 'https://%s%s' % (self.icsp_host, endpoint)
        headers = copy.copy(self.base_headers)
        p = requests.put(url, headers=headers,
                         json=payload, verify=self.icsp_sslverify)
        results = p.json()
        self.check_results(results)
        return

    def icsp_post(self, endpoint, payload):
        url = 'https://%s%s' % (self.icsp_host, endpoint)
        headers = copy.copy(self.base_headers)
        headers['Content-type'] = "application/json"
        p = requests.post(url, headers=headers,
                          data=payload, verify=self.icsp_sslverify)
        results = p.json()
        self.check_results(results)
        return results

    def icsp_delete(self, endpoint):
        url = 'https://%s%s' % (self.icsp_host, endpoint)
        headers = copy.copy(self.base_headers)
        requests.delete(url, headers=headers, verify=self.icsp_sslverify)
        return
