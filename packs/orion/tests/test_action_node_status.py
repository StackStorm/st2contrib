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

from node_status import NodeStatus

__all__ = [
    'NodeStatusTestCase'
]


class NodeStatusTestCase(OrionBaseActionTestCase):
    __test__ = True
    action_cls = NodeStatus

    def test_run_connect_fail(self):
        action = self.setup_connect_fail()
        self.assertRaises(ValueError, action.run, "router1")

    def test_run_node_not_found(self):
        action = self.setup_query_blank_results()
        self.assertRaises(ValueError, action.run, "router1")

    def test_run_node_status_up(self):
        expected = {'node': 'router1 (NodeId: 1; ip: 192.168.0.1)',
                    'status': "Up",
                    'color': "#00ad52"}

        query_data = []
        query_data.append(self.query_npm_node)
        query_data.append(self.query_ncm_node)
        query_data.append({'results': [{'Status': 1}]})

        action = self.get_action_instance(config=self.full_config)
        action.connect = MagicMock(return_value="orion")
        action.query = MagicMock(side_effect=query_data)

        result = action.run("router1")
        self.assertEqual(result, expected)

    def test_run_node_status_down(self):
        expected = {'node': 'router1 (NodeId: 1; ip: 192.168.0.1)',
                    'status': "Down",
                    'color': "#eb0000"}

        query_data = []
        query_data.append(self.query_npm_node)
        query_data.append(self.query_ncm_node)
        query_data.append({'results': [{'Status': 2}]})

        action = self.get_action_instance(config=self.full_config)
        action.connect = MagicMock(return_value="orion")
        action.query = MagicMock(side_effect=query_data)

        result = action.run("router1")
        self.assertEqual(result, expected)

    def test_run_node_status_unknown(self):
        expected = {'node': 'router1 (NodeId: 1; ip: 192.168.0.1)',
                    'status': "Unknown",
                    'color': None}

        query_data = []
        query_data.append(self.query_npm_node)
        query_data.append(self.query_ncm_node)
        query_data.append({'results': [{'Status': 0}]})

        action = self.get_action_instance(config=self.full_config)
        action.connect = MagicMock(return_value="orion")
        action.query = MagicMock(side_effect=query_data)

        result = action.run("router1")
        self.assertEqual(result, expected)

    def test_run_node_status_warning(self):
        expected = {'node': 'router1 (NodeId: 1; ip: 192.168.0.1)',
                    'status': "Warning",
                    'color': "#e89e0e"}

        query_data = []
        query_data.append(self.query_npm_node)
        query_data.append(self.query_ncm_node)
        query_data.append({'results': [{'Status': 3}]})

        action = self.get_action_instance(config=self.full_config)
        action.connect = MagicMock(return_value="orion")
        action.query = MagicMock(side_effect=query_data)

        result = action.run("router1")
        self.assertEqual(result, expected)
