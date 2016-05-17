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

from node_unmanage import NodeUnmanage

__all__ = [
    'NodeUnmanageTestCase'
]


class NodeUnmanageTestCase(OrionBaseActionTestCase):
    __test__ = True
    action_cls = NodeUnmanage

    def test_run_connect_fail(self):
        action = self.setup_connect_fail()
        self.assertRaises(ValueError,
                          action.run,
                          "orion",
                          "router1",
                          30)

    def test_run_node_not_found(self):
        action = self.setup_query_blank_results()
        self.assertRaises(ValueError,
                          action.run,
                          "orion",
                          "router1",
                          30)

    def test_run_unmanaged(self):
        action = self.setup_node_exists()
        self.assertTrue(action.run("router1", "orion", 30))

    def test_run_invoke_returns_text(self):
        expected = "fake"

        query_data = []
        query_data.append(self.query_npm_node)
        query_data.append(self.query_ncm_node)

        action = self.get_action_instance(config=self.full_config)

        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(side_effect=query_data)
        action.invoke = MagicMock(return_value="fake")

        result = action.run("router1",
                            "orion",
                            30)
        self.assertEqual(result, expected)

    def test_run_unmanage_too_long(self):
        action = self.setup_node_exists()
        self.assertRaises(ValueError,
                          action.run,
                          "orion",
                          "router1",
                          90)
