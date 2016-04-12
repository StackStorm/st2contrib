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
from st2actions.runners.pythonrunner import Action


class ICSPBaseActions(Action):

    def __init__(self, config):
        super(ICSPBaseActions, self).__init__(config)
        self.icsp_host = config['host']
        self.icsp_user = config['user']
        self.icsp_pass = config['pass']
        self.icsp_apiv = config['apiv']
        self.icsp_sslverify = config['sslverify']

    def checkResults(self, results):
        # Check for errorCode json element
        if 'errorCode' in results:
            raise Exception("Error: %s" % (results["recommendedActions"]))

    def setConnection(self, connection):
        if 'host' in connection:
            self.icsp_host = connection['host']
        if 'user' in connection:
            self.icsp_user = connection['user']
        if 'pass' in connection:
            self.icsp_pass = connection['pass']

    def getSessionID(self):
        url = 'https://%s/rest/login-sessions' % self.icsp_host
        payload = {'userName': self.icsp_user, 'password': self.icsp_pass}
        headers = {'accept': 'application/json',
                   'accept-language': 'en-us',
                   'Content-Type': 'application/json'}
        p = requests.post(url, headers=headers,
                          json=payload, verify=self.icsp_sslverify)
        results = p.json()
        self.checkResults(results)
        self.icsp_sessionid = results["sessionID"]
        return results["sessionID"]

    def icspGET(self, endpoint):
        url = 'https://%s%s' % (self.icsp_host, endpoint)
        headers = {'Auth': self.icsp_sessionid,
                   'X-Api-Version': self.icsp_apiv}
        p = requests.get(url, headers=headers, verify=self.icsp_sslverify)
        results = p.json()
        self.checkResults(results)
        return results

    def icspPUT(self, endpoint, payload):
        url = 'https://%s%s' % (self.icsp_host, endpoint)
        headers = {'Auth': self.icsp_sessionid,
                   'X-Api-Version': self.icsp_apiv}
        p = requests.put(url, headers=headers,
                         json=payload, verify=self.icsp_sslverify)
        results = p.json()
        self.checkResults(results)
        return

    def icspPOST(self, endpoint, payload):
        url = 'https://%s%s' % (self.icsp_host, endpoint)
        headers = {'Auth': self.icsp_sessionid,
                   'X-Api-Version': self.icsp_apiv,
                   'Content-type': "application/json"}
        p = requests.post(url, headers=headers,
                          data=payload, verify=self.icsp_sslverify)
        results = p.json()
        self.checkResults(results)
        return results

    def icspDELETE(self, endpoint):
        url = 'https://%s%s' % (self.icsp_host, endpoint)
        headers = {'Auth': self.icsp_sessionid,
                   'X-Api-Version': self.icsp_apiv}
        requests.delete(url, headers=headers, verify=self.icsp_sslverify)
        return
