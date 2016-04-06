#!/usr/bin/env python

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

import re

from lib.actions import OrionBaseAction


class NodeCreate(OrionBaseAction):
    def run(self,
            node,
            platform,
            ip_address,
            engineID,
            mon_protocol,
            std_community,
            community,
            status):
        """
        Create an node in an Orion monitoring platform.
        """
        results = {}

        # Sort out which platform & poller to create the node on.
        if platform is None:
            try:
                platform = self.config['defaults']['platform']
            except IndexError:
                raise ValueError("No default Orion platform.")

        self.logger.info("Connecting to Orion platform: {}".format(platform))
        self.connect(platform)
        results['platform'] = platform

        # Check node / ip is not already on platform.
        self.logger.info(
            "Checking node ({}) is not on Orion platform: {}".format(node,
                                                                     platform))

        # The API allows addition of duplicate nodes, so check and raise
        # exception if it's already monitored (by name or IP address).
        # FIX ME - Do check of node caption here...
        # FIX ME - Do check of ip caption here...

        kargs = {'Caption': node,
                 'EngineID': engineID,
                 'IPAddress': ip_address
                 }

        if mon_protocol == "snmpv2":
            kargs['ObjectSubType'] = "SNMP"
            kargs['SNMPVersion'] = 2

        if community is not None:
            kargs['Community'] = community
        elif std_community is not None:
            kargs['Community'] = self.config['defaults']['snmp'][std_community]
        elif std_community is None:
            raise ValueError("Need one of community or std_community")

        self.logger.info("Creating Orion Node: {}".format(kargs))
        orion_data = self.create('Orion.Nodes', **kargs)

        results['node_id'] = re.search('(\d+)$', orion_data).group(0)

        self.logger.info("Created Orion Node: {}".format(results['node_id']))

        return results
