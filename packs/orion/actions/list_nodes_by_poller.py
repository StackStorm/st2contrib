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
from lib.utils import status_text_to_code


class ListNodeByPoller(OrionBaseAction):
    def run(self, poller="primary", status="Up", whitelist=None):
        """
        Lists the Orion Nodes (optionally by State) on an Orion Poller.

        Args:
        - poller: The Orion poller to list nodes on (default: primary)

        Returns:
        - dict: Of data from Orion.

        Raises:
        - UserWarning: If poller does not exist.
        """

        results = {'nodes': []}

        self.connect()

        engine_id = self.get_engine_id(poller)

        swql = """SELECT Caption
        FROM Orion.Nodes
        WHERE EngineID=@EngineID
        """

        kargs = {'EngineID': engine_id}

        if not status == "Any":
            status_id = status_text_to_code(status)
            swql += " and Status=@Status"
            kargs['Status'] = status_id

        orion_data = self.query(swql, **kargs)

        for node in orion_data['results']:
            if not whitelist:
                results['nodes'].append(node['Caption'])
            else:
                if node['Caption'] in whitelist:
                    results['nodes'].append(node['Caption'])
        else:
            results['count'] = len(results['nodes'])

        # Will check whitelist & regex here

        return results
