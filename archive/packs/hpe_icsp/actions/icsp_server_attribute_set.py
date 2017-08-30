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


class SetServerAttribute(ICSPBaseActions):
    def run(self, mid, attribute_key, function,
            attribute_value=None, connection_details=None):

        self.set_connection(connection_details)
        self.get_sessionid()
        endpoint = "/rest/os-deployment-servers/%s" % (mid)
        payload = {"category": "os-deployment-servers",
                   "customAttributes": [], "type": "OSDServer"}
        if function == "Add":
            payload["customAttributes"].append(
                {"key": attribute_key, "values": [
                    {"scope": "server", "value": attribute_value}]})

        # If function is set to append any undefined attributes from server
        # any attribute to replace must be defined in full in the new call

        currentdetails = self.icsp_get(endpoint)
        payload["name"] = currentdetails['name']
        for element in currentdetails['customAttributes']:
            if element['values'][0]['scope'] == 'server'\
                    and not element['key'].startswith("__"):
                if function == "Delete" and element['key'] == attribute_key:
                    continue
                else:
                    if element['key'] != attribute_key:
                        oldatt = {"key": element['key'], "values": [
                            {"scope": "server",
                             "value": element['values'][0]['value']}]}
                        payload['customAttributes'].append(oldatt)

        try:
            self.icsp_put(endpoint, payload)
        except Exception as e:
            raise Exception("Error: %s" % e)
        return
