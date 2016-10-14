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

from st2tests.base import BaseActionAliasTestCase


class StartDiscovery(BaseActionAliasTestCase):
    action_alias_name = "start_discovery"

    def test_start_discovery(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "orion start discovery name run-import nodes 192.168.1.1 snmp public,private"  # NOQA
        expected_parameters = {
            'name': "run-import",
            'nodes': "192.168.1.1",
            'poller': 'primary',
            'snmp_communities': "public,private",
        }
        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

    def test_start_discovery_poller(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "orion start discovery name run-import nodes 192.168.1.1 snmp public,private poller2"  # NOQA
        expected_parameters = {
            'name': "run-import",
            'nodes': "192.168.1.1",
            'poller': 'poller2',
            'snmp_communities': "public,private",
        }
        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)


class NcmConfigDownloadActionAliasTestCase(BaseActionAliasTestCase):
    action_alias_name = 'ncm_config_download'

    def test_ncm_config_download_alias(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "orion ncm config-download router1"
        expected_parameters = {
            'node': 'router1'
        }
        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)


class NodeStatusActionAliasTestCase(BaseActionAliasTestCase):
    action_alias_name = 'node_status'

    def test_node_status_alias(self):
        format_strings = self.action_alias_db.get_format_strings()

        format_string = self.action_alias_db.formats[0]['representation'][0]
        command = "orion node status router1"
        expected_parameters = {
            'node': 'router1'
        }
        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)


class NodeCreateActionAliasTestCase(BaseActionAliasTestCase):
    action_alias_name = 'node_create'

    def test_node_create_alias(self):
        format_strings = self.action_alias_db.get_format_strings()

        # First Format 'orion node create'
        format_string = self.action_alias_db.formats[0]['representation'][0]
        command = "orion node create router1 ip 192.168.0.1 snmp read"
        expected_parameters = {
            'ip_address': "192.168.0.1",
            'node': 'router1',
            'poller': 'primary',
            'community': 'read'
        }
        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

        command = "orion node create router1 ip 192.168.0.1 poller1"
        expected_parameters = {
            'ip_address': "192.168.0.1",
            'node': 'router1',
            'poller': 'poller1',
            'community': None
        }
        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

        command = "orion node create router1 ip 192.168.0.1 snmp read"
        expected_parameters = {
            'ip_address': "192.168.0.1",
            'node': 'router1',
            'poller': 'primary',
            'community': 'read'
        }
        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

        command = "orion node create router1 ip 192.168.0.1"
        expected_parameters = {
            'ip_address': "192.168.0.1",
            'node': 'router1',
            'poller': 'primary',
            'community': None
        }
        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

        # Second format 'create orion node'
        format_string = self.action_alias_db.formats[1]['representation'][0]

        command = "create orion node router1 at 192.168.0.1 with read on poller1"
        expected_parameters = {
            'ip_address': "192.168.0.1",
            'node': 'router1',
            'poller': 'poller1',
            'community': 'read'
        }
        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

        command = "create orion node router1 at 192.168.0.1 with read"
        expected_parameters = {
            'ip_address': "192.168.0.1",
            'node': 'router1',
            'poller': 'primary',
            'community': 'read'
        }
        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

        command = "create orion node router1 at 192.168.0.1"
        expected_parameters = {
            'ip_address': "192.168.0.1",
            'node': 'router1',
            'poller': 'primary',
            'community': None
        }
        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

        command = "create orion node router1 at 192.168.0.1"
        expected_parameters = {
            'ip_address': "192.168.0.1",
            'node': 'router1',
            'poller': 'primary',
            'community': None
        }
        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)
