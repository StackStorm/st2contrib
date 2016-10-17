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


from add_node_to_ncm import AddNodeToNCM

__all__ = [
    'AddNodeToNCMTestCase'
]


class AddNodeToNCMTestCase(OrionBaseActionTestCase):
    __test__ = True
    action_cls = AddNodeToNCM

    def test_run_connect_fail(self):
        action = self.setup_connect_fail()
        self.assertRaises(ValueError,
                          action.run,
                          "router1")

    def test_run_node_not_in_npm(self):
        action = self.setup_query_blank_results()
        self.assertRaises(UserWarning,
                          action.run,
                          "router1")

    def test_run_node_already_in_ncm(self):
        action = self.setup_node_exists()
        self.assertRaises(UserWarning,
                          action.run,
                          "router1")

    def test_run_add_node_to_ncm(self):
        expected = "abc-1234"

        query_data = []
        query_data.append(self.query_npm_node)
        query_data.append(self.query_no_results)

        action = self.get_action_instance(config=self.full_config)
        action.connect = MagicMock(return_value="orion")
        action.query = MagicMock(side_effect=query_data)
        action.invoke = MagicMock(return_value="abc-1234")

        result = action.run("router1")
        self.assertEqual(result, expected)
