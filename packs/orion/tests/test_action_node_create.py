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

from mock import MagicMock

from orion_base_action_test_case import OrionBaseActionTestCase

from node_create import NodeCreate
from lib.utils import is_ip


__all__ = [
    'NodeCreateTestCase'
]


class NodeCreateTestCase(OrionBaseActionTestCase):
    __test__ = True
    action_cls = NodeCreate

    def test_run_is_ip_v4(self):
        self.assertTrue(is_ip("172.16.0.1"))
        self.assertTrue(is_ip("1762:0:0:0:0:B03:1:AF18"))
        self.assertFalse(is_ip("172.16.0.300"))
        self.assertFalse(is_ip("1762:%:0:0:0:B03:1:AF18"))
        self.assertFalse(is_ip("server.example.com"))
        self.assertFalse(is_ip("router1"))
        self.assertFalse(is_ip("router:8080"))

    def test_run_connect_fail(self):
        action = self.setup_connect_fail()
        self.assertRaises(ValueError,
                          action.run,
                          "router1",
                          "192.168.0.1",
                          None,
                          "snmpv2",
                          "internal",
                          "snmp")

    def test_run_node_caption_exists(self):
        action = self.setup_node_exists()
        self.assertRaises(ValueError,
                          action.run,
                          "router1",
                          "192.168.0.1",
                          None,
                          "snmpv2",
                          "internal",
                          "snmp")

    def test_run_node_ip_exists(self):
        query_data = []
        query_data.append(self.query_no_results)
        query_data.append(self.query_npm_node)
        query_data.append(self.query_ncm_node)

        action = self.get_action_instance(config=self.full_config)

        action.connect = MagicMock(return_value="orion")
        action.query = MagicMock(side_effect=query_data)
        action.invoke = MagicMock(return_value=None)
        action.create = MagicMock(return_value=None)

        self.assertRaises(ValueError,
                          action.run,
                          "router2",
                          "192.168.0.1",
                          None,
                          "snmpv2",
                          "internal",
                          "snmp")

    def test_run_get_snmp_community(self):
        action = self.get_action_instance(config=self.full_config)

        self.assertEqual(action.get_snmp_community(None), "publ1c")
        self.assertEqual(action.get_snmp_community("customer"), "foobar")
        self.assertEqual(action.get_snmp_community("internal"), "barbaz")
        self.assertEqual(action.get_snmp_community("bazfoo"), "bazfoo")

    def test_run_poller_is_none(self):
        expected = {'node_id': '6',
                    'label': 'orion'}

        query_data = self.query_no_results

        action = self.get_action_instance(config=self.full_config)

        action.connect = MagicMock(return_value="orion")
        action.query = MagicMock(return_value=query_data)
        action.invoke = MagicMock(return_value=None)
        action.get_engine_id = MagicMock(return_value=2)
        action.create = MagicMock(
            return_value="swis://orionr/Orion/Orion.Nodes/NodeID=6")

        result = action.run("router2",
                            "192.168.0.1",
                            None,
                            "snmpv2",
                            "internal",
                            "snmp")
        self.assertEqual(result, expected)

    def test_run_node_additonal_poller(self):
        expected = {'node_id': '6',
                    'label': 'orion'}

        query_data = [self.query_no_results,
                      self.query_no_results,
                      {'results': [{'EngineID': 2}]}]

        action = self.get_action_instance(config=self.full_config)

        action.connect = MagicMock(return_value="orion")
        action.query = MagicMock(side_effect=query_data)
        action.invoke = MagicMock(return_value=None)
        action.create = MagicMock(
            return_value="swis://orionr/Orion/Orion.Nodes/NodeID=6")

        result = action.run("router2",
                            "192.168.0.1",
                            "additonal1",
                            "snmpv2",
                            "internal",
                            "snmp")
        self.assertEqual(result, expected)
