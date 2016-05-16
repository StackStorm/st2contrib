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

import yaml
from mock import Mock, MagicMock

from st2tests.base import BaseActionTestCase

from node_create import NodeCreate
from lib.utils import is_ip


__all__ = [
    'NodeCreateTestCase'
]


class NodeCreateTestCase(BaseActionTestCase):
    action_cls = NodeCreate

    def test_run_is_ip_v4(self):
        self.assertTrue(is_ip("172.16.0.1"))
        self.assertTrue(is_ip("1762:0:0:0:0:B03:1:AF18"))
        self.assertFalse(is_ip("172.16.0.300"))
        self.assertFalse(is_ip("1762:%:0:0:0:B03:1:AF18"))

    def test_run_no_config(self):
        self.assertRaises(ValueError,
                          NodeCreate,
                          yaml.safe_load(
                              self.get_fixture_content('blank.yaml')))

    def test_run_is_instance(self):
        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        self.assertIsInstance(action, NodeCreate)

    def test_run_connect_fail(self):
        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        action.connect = Mock(side_effect=ValueError(
            'Orion host details not in the config.yaml'))

        self.assertRaises(ValueError,
                          action.run,
                          "router1",
                          "192.168.0.1",
                          "orion",
                          None,
                          "snmpv2",
                          "internal",
                          None,
                          "snmp")

    def test_run_node_caption_exists(self):
        query_data = []
        query_data.append(yaml.safe_load(
            self.get_fixture_content("orion_npm_results.yaml")))
        query_data.append(yaml.safe_load(
            self.get_fixture_content("orion_ncm_results.yaml")))

        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(side_effect=query_data)
        action.invoke = Mock(return_value=None)
        action.create = Mock(return_value=None)

        self.assertRaises(ValueError,
                          action.run,
                          "router1",
                          "192.168.0.1",
                          "orion",
                          None,
                          "snmpv2",
                          "internal",
                          None,
                          "snmp")

    def test_run_node_ip_exists(self):
        query_data = []
        query_data.append({'results': []})
        query_data.append(yaml.safe_load(
            self.get_fixture_content("orion_npm_results.yaml")))
        query_data.append(yaml.safe_load(
            self.get_fixture_content("orion_ncm_results.yaml")))

        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(side_effect=query_data)
        action.invoke = MagicMock(return_value=None)
        action.create = MagicMock(return_value=None)

        self.assertRaises(ValueError,
                          action.run,
                          "router2",
                          "192.168.0.1",
                          "orion",
                          None,
                          "snmpv2",
                          "internal",
                          None,
                          "snmp")

    def test_run_poller_is_none(self):
        expected = {'node_id': '6', 'platform': 'orion'}

        query_data = {'results': []}

        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(return_value=query_data)
        action.invoke = MagicMock(return_value=None)
        action.get_engine_id = MagicMock(return_value=2)
        action.create = MagicMock(
            return_value="swis://orionr/Orion/Orion.Nodes/NodeID=6")

        result = action.run("router2",
                            "192.168.0.1",
                            "orion",
                            None,
                            "snmpv2",
                            "internal",
                            None,
                            "snmp")
        self.assertEqual(result, expected)

    def test_run_node_additonal_poller(self):
        expected = {'node_id': '6', 'platform': 'orion'}

        query_data = [{'results': []},
                      {'results': []},
                      {'results': [{'EngineID': 2}]}]

        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(side_effect=query_data)
        action.invoke = MagicMock(return_value=None)
        action.create = MagicMock(
            return_value="swis://orionr/Orion/Orion.Nodes/NodeID=6")

        result = action.run("router2",
                            "192.168.0.1",
                            "orion",
                            "additonal1",
                            "snmpv2",
                            "internal",
                            None,
                            "snmp")
        self.assertEqual(result, expected)
