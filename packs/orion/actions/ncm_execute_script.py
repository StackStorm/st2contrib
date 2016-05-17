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

from lib.actions import OrionBaseAction


class NcmExecuteScript(OrionBaseAction):
    def run(self, platform, node, script):
        """
        Excute an Orion NCM script on a node.

        Args:
            platform
            node
            script

        Returns:
            Output

        Raises:
            ValueError: If Node is not in NCM.
        """
        results = {}

        self.connect(platform)

        orion_node = self.get_node(node)

        if not orion_node.npm:
            raise ValueError("Node not found in NPM {}".format(
                orion_node.caption))

        if not orion_node.ncm:
            raise ValueError("Node not found in NCM {}".format(
                orion_node.caption))

        orion_data = self.invoke(
            "Cirrus.ConfigArchive",
            "ExecuteScript",
            [orion_node.ncm_id],
            "show failover")
        results['job_id'] = orion_data[0]

        results['transfer'] = self.get_ncm_transfer_results(
            results['job_id'])

        return results
