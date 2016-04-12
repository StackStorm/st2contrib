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

from lib.icsp import ICSPBaseActions


class SetServerAttributes(ICSPBaseActions):
    def run(self, mid, connection_details, attributes, function):
        if connection_details:
            self.setConnection(connection_details)
        self.getSessionID()
        endpoint = "/rest/os-deployment-servers/%s" % mid
        payload = {"category": "os-deployment-servers",
                   "customAttributes": [], "type": "OSDServer"}
        for attribute in attributes:
            payload["customAttributes"].append(
                {"key": attribute, "values": [
                    {"scope": "server", "value": attributes[attribute]}]})

        # If function is set to append any undefined attributes from server
        # any attribute to replace must be defined in full in the new call

        if function == "append":
            currentdetails = self.icspGET(endpoint)
            for element in currentdetails['customAttributes']:
                if element['values'][0]['scope'] == 'server'\
                        and not element['key'].startswith("__"):
                    oldatt = {"key": element['key'], "values": [
                        {"scope": "server",
                         "value": element['values'][0]['value']}]}
                    if oldatt not in payload['customAttributes']:
                        payload['customAttributes'].append(oldatt)

        try:
            self.icspPUT(endpoint, payload)
        except Exception as e:
            raise Exception("Error: %s" % e)
        return
