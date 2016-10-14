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

from datetime import datetime, timedelta

from lib.actions import OrionBaseAction


class NodeUnmanage(OrionBaseAction):
    def run(self, node, minutes):
        """
        Unmanage an Orion node
        """

        if minutes > self.config['unmanage_max']:
            raise ValueError(
                "minutes ({}) greater than unmanage_max ({})".format(
                    minutes, self.config['unmanage_max']))

        self.connect()

        orion_node = self.get_node(node)

        if not orion_node.npm:
            raise ValueError("Node not found")

        NodeId = "N:{}".format(orion_node.npm_id)
        now = datetime.utcnow()
        later = now + timedelta(minutes=minutes)

        orion_data = self.invoke("Orion.Nodes",
                                 "Unmanage",
                                 NodeId,
                                 now,
                                 later,
                                 False)

        # This Invoke always returns None, so check and return True
        if orion_data is None:
            return True
        else:
            return orion_data
