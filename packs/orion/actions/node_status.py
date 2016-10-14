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
from lib.utils import status_code_to_text, send_user_error


class NodeStatus(OrionBaseAction):
    def run(self, node):
        """
        Query Solarwinds Orion.
        """

        # Set up the results
        results = {}
        results['status'] = None
        results['color'] = None

        self.connect()

        orion_node = self.get_node(node)

        if not orion_node.npm:
            error_msg = "Node not found"
            send_user_error(error_msg)
            raise ValueError(error_msg)

        swql = "SELECT Status FROM Orion.Nodes WHERE NodeID=@NodeID"
        kargs = {'NodeID': orion_node.npm_id}
        orion_data = self.query(swql, **kargs)

        (results['status'], results['color']) = status_code_to_text(
            orion_data['results'][0]['Status'])
        results['node'] = str(orion_node)

        return results
