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
from lib.utils import send_user_error


class ListNodeCustomProperties(OrionBaseAction):
    def run(self, node, platform):
        """
        Lists the Orion Custom Properties on an Node.

        Args:
            node: The caption in Orion of the node to poll.
            platform: The orion platform to act on.

        Returns:
            dict: Of data from Orion.

        Raises:
            UserWarning: If node does not exist.
        """

        self.connect(platform)

        orion_node = self.get_node(node)

        if not orion_node.npm:
            msg = "Node not in Orion NPM: {}".format(node)
            send_user_error(msg)
            raise UserWarning(msg)

        orion_data = self.read(orion_node.uri + '/CustomProperties')

        return orion_data
