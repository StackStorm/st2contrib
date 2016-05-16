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

from node_unmanage import NodeUnmanage

__all__ = [
    'NodeUnmanageTestCase'
]


class NodeUnmanageTestCase(BaseActionTestCase):
    action_cls = NodeUnmanage

    def test_run_no_config(self):
        self.assertRaises(ValueError,
                          NodeUnmanage,
                          yaml.safe_load(
                              self.get_fixture_content('blank.yaml')))

    def test_run_is_instance(self):
        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        self.assertIsInstance(action, NodeUnmanage)

    def test_run_connect_fail(self):
        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        action.connect = Mock(side_effect=ValueError(
            'Orion host details not in the config.yaml'))

        self.assertRaises(ValueError,
                          action.run,
                          "orion",
                          "router1",
                          30)

    def test_run_node_not_found(self):
        query_data = []
        query_data.append({'results': []})
        query_data.append({'results': []})

        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(side_effect=query_data)

        self.assertRaises(ValueError,
                          action.run,
                          "orion",
                          "router1",
                          30)

    def test_run_unmanaged(self):
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

        result = action.run("router1",
                            "orion",
                            30)

        self.assertTrue(result)

    def test_run_invoke_returns_text(self):
        expected = "fake"

        query_data = []
        query_data.append(yaml.safe_load(
            self.get_fixture_content("orion_npm_results.yaml")))
        query_data.append(yaml.safe_load(
            self.get_fixture_content("orion_ncm_results.yaml")))

        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(side_effect=query_data)
        action.invoke = MagicMock(return_value="fake")

        result = action.run("router1",
                            "orion",
                            30)

        self.assertEqual(result, expected)

    def test_run_unmanage_too_long(self):
        query_data = []
        query_data.append(yaml.safe_load(
            self.get_fixture_content("orion_npm_results.yaml")))
        query_data.append(yaml.safe_load(
            self.get_fixture_content("orion_ncm_results.yaml")))

        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        action.connect = Mock(return_value=True)
        action.query = MagicMock(side_effect=query_data)
        action.invoke = Mock(side_effect=True)

        self.assertRaises(ValueError,
                          action.run,
                          "orion",
                          "router1",
                          90)
