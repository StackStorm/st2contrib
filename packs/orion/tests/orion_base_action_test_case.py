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
from mock import MagicMock

from st2tests.base import BaseActionTestCase


class OrionBaseActionTestCase(BaseActionTestCase):
    __test__ = False

    def setUp(self):
        super(OrionBaseActionTestCase, self).setUp()

        self._blank_config = self.load_yaml('blank.yaml')
        self._full_config = self.load_yaml('full.yaml')
        self._query_npm_node = self.load_yaml('orion_npm_results.yaml')
        self._query_ncm_node = self.load_yaml('orion_ncm_results.yaml')

    def load_yaml(self, filename):
        return yaml.safe_load(self.get_fixture_content(filename))

    @property
    def blank_config(self):
        return self._blank_config

    @property
    def full_config(self):
        return self._full_config

    @property
    def query_npm_node(self):
        return self._query_npm_node

    @property
    def query_ncm_node(self):
        return self._query_ncm_node

    @property
    def query_no_results(self):
        return {'results': []}

    def setup_connect_fail(self):
        action = self.get_action_instance(config=self.full_config)

        action.connect = MagicMock(side_effect=ValueError(
            'Orion host details not in the config.yaml'))

        return action

    def setup_query_blank_results(self):
        query_data = [self.query_no_results]

        action = self.get_action_instance(config=self.full_config)

        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(side_effect=query_data)

        return action

    def setup_node_exists(self):
        query_data = []
        query_data.append(self.query_npm_node)
        query_data.append(self.query_ncm_node)

        action = self.get_action_instance(config=self.full_config)

        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(side_effect=query_data)
        action.invoke = MagicMock(return_value=None)
        action.update = MagicMock(return_value=None)

        return action

    def test_run_no_config(self):
        self.assertRaises(ValueError,
                          self.action_cls,
                          self.blank_config)

    def test_run_is_instance(self):
        action = self.get_action_instance(self.full_config)
        self.assertIsInstance(action, self.action_cls)
