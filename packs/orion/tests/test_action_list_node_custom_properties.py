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
# from mock import Mock, MagicMock

from st2tests.base import BaseActionTestCase

from list_node_custom_properties import ListNodeCustomProperties

__all__ = [
    'ListNodeCustomProperties'
]

MOCK_CONFIG_BLANK = yaml.safe_load(open(
    'packs/orion/tests/fixture/blank.yaml').read())
MOCK_CONFIG_FULL = yaml.safe_load(open(
    'packs/orion/tests/fixture/full.yaml').read())


class ListNodeCustomPropertiesTestCase(BaseActionTestCase):
    action_cls = ListNodeCustomProperties

    def test_run_no_config(self):
        self.assertRaises(ValueError,
                          ListNodeCustomProperties,
                          MOCK_CONFIG_BLANK)

    def test_run_is_instance(self):
        action = self.get_action_instance(MOCK_CONFIG_FULL)

        self.assertIsInstance(action, ListNodeCustomProperties)
