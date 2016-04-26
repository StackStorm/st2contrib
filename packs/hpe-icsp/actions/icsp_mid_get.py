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


class GetMid(ICSPBaseActions):
    def run(self, uuid=None, serialnumber=None, connection_details=None):

        self.set_connection(connection_details)
        self.get_sessionid()
        endpoint = "/rest/os-deployment-servers"
        getresults = self.icsp_get(endpoint)
        servers = getresults["members"]
        results = []
        # Checking arrays are set otherwise errors occur later
        # when called within flows missing arrays cause python errors
        if not serialnumber:
            serialnumber = []
        if not uuid:
            uuid = []
        for server in servers:
            if (server["uuid"] in uuid) or\
                    (server["serialNumber"] in serialnumber):
                if (len(uuid) + len(serialnumber)) == 1:
                    return {'mid': int(server["mid"])}
                else:
                    if server["mid"] not in results:
                        results.append(int(server["mid"]))

        if results:
            return results
        else:
            raise ValueError("No Servers Found")
