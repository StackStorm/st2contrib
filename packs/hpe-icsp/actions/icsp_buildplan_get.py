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


class GetBuildPlans(ICSPBaseActions):
    def run(self, plan_names=None, connection_details=None):
        self.set_connection(connection_details)
        self.get_sessionid()

        endpoint = "/rest/os-deployment-build-plans"
        results = self.icsp_get(endpoint)
        plans = []
        for plan in results["members"]:
            if plan_names:
                for name in plan_names:
                    if name.lower() == str(plan["name"]).lower():
                        uri = self.extract_id(plan["uri"])
                        plans.append({"name": plan["name"], "uri": uri})
            else:
                uri = self.extract_id(plan["uri"])
                plans.append({"name": plan["name"], "uri": uri})

        return {"plans": plans}
