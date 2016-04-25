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


class NcmConfigDownloadActionAliasTestCase(BaseActionAliasTestCase):
    action_alias_name = 'ncm_config_download'

    def test_ncm_config_download_alias(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "orion ncm config-download orion router1"
        expected_parameters = {
            'platform': 'orion',
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
        command = "orion node status orion router1"
        expected_parameters = {
            'platform': 'orion',
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
        command = "orion node create router1 ip 192.168.0.1 snmp read platform orion"
        expected_parameters = {
            'ip_address': "192.168.0.1",
            'node': 'router1',
            'platform': 'orion',
            'poller': 'primary',
            'std_community': 'read'
        }
        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

        command = "orion node create router1 ip 192.168.0.1 platform orion poller1"
        expected_parameters = {
            'ip_address': "192.168.0.1",
            'node': 'router1',
            'platform': 'orion',
            'poller': 'poller1',
            'std_community': None
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
            'platform': None,
            'poller': 'primary',
            'std_community': 'read'
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
            'platform': None,
            'poller': 'primary',
            'std_community': None
        }
        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

        # Second format 'create orion node'
        format_string = self.action_alias_db.formats[1]['representation'][0]

        command = "create orion node router1 at 192.168.0.1 with read on orion poller1"
        expected_parameters = {
            'ip_address': "192.168.0.1",
            'node': 'router1',
            'platform': 'orion',
            'poller': 'poller1',
            'std_community': 'read'
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
            'platform': None,
            'poller': 'primary',
            'std_community': 'read'
        }
        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

        command = "create orion node router1 at 192.168.0.1 on orion"
        expected_parameters = {
            'ip_address': "192.168.0.1",
            'node': 'router1',
            'platform': 'orion',
            'poller': 'primary',
            'std_community': None
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
            'platform': None,
            'poller': 'primary',
            'std_community': None
        }
        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)
