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
import json


class ApplyBuildPlan(ICSPBaseActions):
    def run(self, buildplan_ids, server_data, connection_details=None):
        self.set_connection(connection_details)
        self.get_sessionid()

        # Prepare Endpoint within ICSP API
        endpoint = "/rest/os-deployment-jobs"

        # Prepare Pesonality Data data collection
        pload = {}
        pload['osbpUris'] = []
        pload['failMode'] = None
        pload['serverData'] = []

        for plan in buildplan_ids:
            # Confirm input are integers
            try:
                isinstance(plan, int)
            except:
                raise ValueError("Build plans must be \
                                 Integers (comma seperated)")

            pload["osbpUris"].append("/rest/os-deployment-build-plans/%s"
                                     % (plan))

        for server in server_data:
            data = {}
            pdata = {}
            data['serverUri'] = "/rest/os-deployment-servers/%s" % (server)

            # Prepare server personality Data
            # Initially not including network data Although
            # this can be included later
            # TODO extend variable values to include IP configuration

            if "hostname" in server_data[server]:
                pdata['hostName'] = server_data[server]['hostname']
            if "domain" in server_data[server]:
                pdata['domain'] = server_data[server]['domain']
            if "workgroup" in server_data[server]:
                pdata['workgroup'] = server_data[server]['workgroup']
            data['personalityData'] = pdata

            pload['serverData'].append(data)

        payload = json.dumps(pload)
        try:
            results = self.icsp_post(endpoint, payload)
        except Exception as e:
            raise Exception("Error: %s" % e)

        return {"jobid": self.extract_id(results['uri'])}
