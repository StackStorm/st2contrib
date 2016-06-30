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

import time

from lib.actions import OrionBaseAction
from lib.utils import send_user_error


class NodesPollNow(OrionBaseAction):
    def run(self, nodes, platform, count, pause):
        """
        Invoke a PollNow verb against a Orion Node.

        Args:
        - node: The caption in Orion of the node to poll.
        - platform: The orion platform to act on.
        - count: Number of polls to complete.
        - pause: Number of seconds to wait between each cycle.

        Returns
            True: As PollNow does not return any data.

        Raises:
            IndexError: When a nodes is not found.
        """

        self.connect(platform)
        orion_nodes = []

        for node in nodes:
            orion_node = self.get_node(node)

            if orion_node.npm:
                orion_nodes.append(orion_node.npm_id)
            else:
                error_msg = "Node not found"
                send_user_error(error_msg)
                raise ValueError(error_msg)

        for c in range(count):
            for npm_id in orion_nodes:
                self.invoke("Orion.Nods",
                            "PollNow",
                            npm_id)
            else:
                time.sleep(pause)

        # These Invoke's return None, so we just return True
        return True
