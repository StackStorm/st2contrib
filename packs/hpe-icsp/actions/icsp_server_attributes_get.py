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


class GetServerAttributes(ICSPBaseActions):
    def run(self, mids, connection_details=None,
            attribute_key=None, attribute_type="all"):
        self.set_connection(connection_details)
        self.get_sessionid()
        endpoint = "/rest/os-deployment-servers"
        results = {}
        for mid in mids:
            try:
                isinstance(mid, int)
            except:
                raise ValueError("MIDs must be integers")
            getreq = self.icsp_get(endpoint + "/%s" % (mid))
            allattr = getreq['customAttributes']
            results[mid] = allattr

        output = results

        # Filter based on Attribute Type
        if not attribute_type == "all":
            filtereddata = {}
            for server in results:
                filteredelements = []
                for element in results[server]:
                    if element['values'][0]['scope'] == attribute_type:
                        filteredelements.append(element)
                filtereddata[server] = filteredelements
            output = filtereddata

        # Filter staged results to key words provided
        if attribute_key:
            filtereddata = {}
            for server in output:
                filteredelements = []
                for element in output[server]:
                    if element['key'] == attribute_key:
                        filteredelements.append(element)
                filtereddata[server] = filteredelements
            output = filtereddata

        return {"attributes": output}
