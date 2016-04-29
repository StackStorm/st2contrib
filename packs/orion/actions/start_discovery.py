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


class StartDiscovery(OrionBaseAction):
    def run(self,
            name,
            node,
            ip_address,
            platform,
            poller,
            std_community):
        """
        Create and Start Discovery process in Orion.
        """
        results = {}

        # Sort out which platform & poller to create the node on.
        if platform is None:
            try:
                platform = self.config['defaults']['platform']
            except IndexError:
                self.send_user_error("No default Orion platform.")
                raise ValueError("No default Orion platform.")

        self.logger.info("Connecting to Orion platform: {}".format(platform))
        self.connect(platform)
        results['platform'] = platform

        if self.node_exists(node, ip_address):
            self.logger.error(
                "Node ({}) or IP ({}) already in Orion platform: {}".format(
                    node,
                    ip_address,
                    platform)
            )

            self.send_user_error("Node and/or IP is already in Orion!")
            raise Exception("Node and/or IP already exists!")
        else:
            self.logger.info(
                "Checking node ({}) is not on Orion platform: {}".format(
                    node,
                    platform)
            )

        ## Need to get the CredentialID for the standard community
        ## Can we turn off UDT?

        #self.get_snmp_community(community, std_community))

        CorePluginConfiguration = self.invoke('Orion.Discovery',
                                              'CreateCorePluginConfiguration',
                                              {'BulkList': [{'Address': ip_address}],
                                               # 'IpRanges': [], # Optional
                                               # 'Subnets': None, # Optional
                                               'Credentials': [
                                                   {'CredentialID': 1, 'Order': 1}
                                               ],
                                               'WmiRetriesCount': 0,
                                               'WmiRetryIntervalMiliseconds': 1000})

        # engineID if happens to be None, default to the primary.
        if poller is not None:
            engineID = self.get_engine_id(poller)
        else:
            engineID = 1

        self.logger.info("Triggering Discovery of Orion Node: {} [{}]".format(node, ip_address))

        disco = self.invoke('Orion.Discovery', 'StartDiscovery',
                            {
                                'Name': name,
                                'EngineId': engineID,
                                'JobTimeoutSeconds': 3600,
                                'SearchTimeoutMiliseconds': 2000,
                                'SnmpTimeoutMiliseconds': 2000,
                                'SnmpRetries': 4,
                                'RepeatIntervalMiliseconds': 1800,
                                'SnmpPort': 161,
                                'HopCount': 0,
                                'PreferredSnmpVersion': 'SNMP2c',
                                'DisableIcmp': False,
                                'AllowDuplicateNodes': False,
                                'IsAutoImport': True,
                                'IsHidden': False,
                                'PluginConfigurations': [
                                    {'PluginConfigurationItem': CorePluginConfiguration}
                                ]
                            })

        return disco
