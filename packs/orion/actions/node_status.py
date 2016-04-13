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

from lib.actions import OrionBaseAction


class NodeStatus(OrionBaseAction):
    def run(self, node, platform):
        """
        Query Solarwinds Orion.
        """

        # Set up the results
        results = {}
        results['status'] = None
        results['color'] = None

        self.connect(platform)

        swql = "SELECT Status FROM Orion.Nodes WHERE Caption=@node"
        kargs = {'node': node}
        orion_data = self.query(swql, **kargs)

        if len(orion_data['results']) != 0:
            (results['status'], results['color']) = self.status_code_to_text(
                orion_data['results'][0]['Status'])
        else:
            error_msg = "Node not found"
            self.send_user_error(error_msg)
            raise ValueError(error_msg)

        return results
