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


class ListNodesStatus(OrionBaseAction):
    def run(self, platform, whitelist=None):
        """
        List the Status of Solarwinds Orion Nodes.
        """

        # Set up the results
        results = {"nodes_down": [],
                   "nodes_unknown": [],
                   "nodes_up": []}

        self.connect(platform)

        swql = "SELECT Caption,Status FROM Orion.Nodes"
        kargs = {}
        orion_data = self.query(swql, **kargs)

        #results['raw'] = orion_data

        for node in orion_data['results']:
            if not whitelist is None:
                if not node['Caption'] in whitelist:
                    continue

            if node["Status"] == 1:
                results['nodes_up'].append(node['Caption'])
            elif node["Status"] == 2:
                results['nodes_down'].append(node['Caption'])
            elif node["Status"] == 0:
                results['nodes_unknown'].append(node['Caption'])

        return results
