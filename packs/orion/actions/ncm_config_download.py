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


class NcmConfigDownload(OrionBaseAction):
    def run(self, node, platform, configs):
        """
        Download configurations via Solarwinds Orion NCM.
        see https://github.com/solarwinds/OrionSDK/wiki/NCM-Config-Transfer
        for more information.

        Args:
           node:
           platform:
           configs: Array of Configs to download.

        Returns:
           dict:

        Raises:
           Exception: If Node is not in NPM or NCM.
        """

        results = {}
        node_ids = []

        self.connect(platform)

        orion_node = self.get_node(node)

        if not orion_node.npm:
            error_msg = "Node not in NPM: {}".format(node)
            send_user_error(error_msg)
            raise Exception(error_msg)

        if not orion_node.ncm:
            error_msg = "Node not in NCM: {} ({})".format(node,
                                                          orion_node.npm_id)
            send_user_error(error_msg)
            raise Exception(error_msg)

        node_ids.append(orion_node.ncm_id)

        for config in configs:
            orion_data = self.invoke("Cirrus.ConfigArchive",
                                     "DownloadConfig",
                                     node_ids,
                                     config)
            transfer_id = orion_data[0]
            results[config] = self.get_ncm_transfer_results(transfer_id)

        return results
