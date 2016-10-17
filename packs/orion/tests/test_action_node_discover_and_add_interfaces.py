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

from node_discover_and_add_interfaces import NodeDiscoverAndAddInterfaces

__all__ = [
    'NodeDiscoverAndAddInterfacesTestCase'
]


class NodeDiscoverAndAddInterfacesTestCase(OrionBaseActionTestCase):
    __test__ = True
    action_cls = NodeDiscoverAndAddInterfaces

    def test_run_connect_fail(self):
        action = self.setup_connect_fail()
        self.assertRaises(ValueError,
                          action.run,
                          "router1")

    def test_run_node_not_found(self):
        action = self.setup_query_blank_results()
        self.assertRaises(ValueError,
                          action.run,
                          "router1")

    def test_run_add_interfaces(self):
        expected = {
            'added': [
                {"eth0": 2},
                {"eth1": 3}],
            'existing': [{'lo': 1}]}

        query_data = []
        query_data.append(self.query_npm_node)
        query_data.append(self.query_ncm_node)

        invoke_data = []
        invoke_data.append(self.load_yaml(
            'invoke_DiscoverInterfacesOnNode.yaml'))
        invoke_data.append(self.load_yaml(
            'invoke_AddInterfacesOnNode.yaml'))

        action = self.get_action_instance(config=self.full_config)
        action.connect = MagicMock(return_value="orion")
        action.query = MagicMock(side_effect=query_data)
        action.invoke = MagicMock(side_effect=invoke_data)

        result = action.run("router1")
        self.assertEqual(result, expected)
