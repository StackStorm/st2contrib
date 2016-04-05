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

from node_status import NodeStatus

__all__ = [
    'NodeStatusTestCase'
]

MOCK_CONFIG_BLANK = ""

MOCK_CONFIG_FULL = """
orion:
  host: orion-npm
  user: stanley
  password: foobar
"""


class NodeStatusTestCase(BaseActionTestCase):
    action_cls = NodeStatus

    def test_run_no_config(self):
        config = yaml.safe_load(MOCK_CONFIG_BLANK)

        self.assertRaises(ValueError, NodeStatus, config)

    def test_run_basic_config(self):
        config = yaml.safe_load(MOCK_CONFIG_FULL)

        action = self.get_action_instance(config)
        self.assertIsInstance(action, NodeStatus)

    def test_run_connect_fail(self):
        config = yaml.safe_load(MOCK_CONFIG_FULL)

        action = self.get_action_instance(config)
        action.connect = Mock(side_effect=ValueError(
            'Orion host details not in the config.yaml'))

        self.assertRaises(ValueError, action.run, "router1", "orion")

    def test_run_node_not_found(self):
        orion_data = {'results': []}

        config = yaml.safe_load(MOCK_CONFIG_FULL)
        action = self.get_action_instance(config)
        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(return_value=orion_data)

        self.assertRaises(ValueError, action.run, "router1", "orion")

    def test_run_node_status_up(self):
        expected = {'status': "Up", 'color': "good"}
        orion_data = {'results': [{'Status': 1}]}

        config = yaml.safe_load(MOCK_CONFIG_FULL)
        action = self.get_action_instance(config)
        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(return_value=orion_data)
        result = action.run("router1", "orion")
        self.assertEqual(result, expected)

    def test_run_node_status_down(self):
        expected = {'status': "Down", 'color': "danger"}
        orion_data = {'results': [{'Status': 2}]}

        config = yaml.safe_load(MOCK_CONFIG_FULL)
        action = self.get_action_instance(config)
        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(return_value=orion_data)
        result = action.run("router1", "orion")
        self.assertEqual(result, expected)

    def test_run_node_status_unknown(self):
        expected = {'status': "Unknown", 'color': "grey"}
        orion_data = {'results': [{'Status': 0}]}

        config = yaml.safe_load(MOCK_CONFIG_FULL)
        action = self.get_action_instance(config)
        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(return_value=orion_data)
        result = action.run("router1", "orion")
        self.assertEqual(result, expected)

    def test_run_node_status_warning(self):
        expected = {'status': "Warning", 'color': "warning"}
        orion_data = {'results': [{'Status': 3}]}

        config = yaml.safe_load(MOCK_CONFIG_FULL)
        action = self.get_action_instance(config)
        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(return_value=orion_data)
        result = action.run("router1", "orion")
        self.assertEqual(result, expected)
