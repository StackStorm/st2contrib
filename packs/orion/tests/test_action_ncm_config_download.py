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

from ncm_config_download import NcmConfigDownload

__all__ = [
    'NcmConfigDownloadTestCase'
]

MOCK_CONFIG_BLANK = yaml.safe_load(open(
    'packs/orion/tests/fixture/blank.yaml').read())
MOCK_CONFIG_FULL = yaml.safe_load(open(
    'packs/orion/tests/fixture/full.yaml').read())


class NcmConfigDownloadTestCase(BaseActionTestCase):
    action_cls = NcmConfigDownload

    def test_run_no_config(self):
        self.assertRaises(ValueError, NcmConfigDownload, MOCK_CONFIG_BLANK)

    def test_run_basic_config(self):
        action = self.get_action_instance(MOCK_CONFIG_FULL)
        self.assertIsInstance(action, NcmConfigDownload)

    def test_run_connect_fail(self):
        action = self.get_action_instance(MOCK_CONFIG_FULL)
        action.connect = Mock(side_effect=ValueError(
            'Orion host details not in the config.yaml'))

        self.assertRaises(ValueError,
                          action.run,
                          "router1",
                          "orion",
                          ["running", "startup"])

    def test_run_ncm_node_not_found(self):
        orion_data = {'results': []}

        action = self.get_action_instance(MOCK_CONFIG_FULL)
        action.connect = MagicMock(return_value=True)

        action.query = MagicMock(return_value=orion_data)

        self.assertRaises(IndexError,
                          action.run,
                          "router1",
                          "orion",
                          ["running", "startup"])

    def test_run_ncm_download_complete(self):
        expected = {'running': {'status': 'Complete'},
                    'startup': {'status': 'Complete'}
                    }
        query_data = [
            {'results': [{'NodeID': "abc1234"}]},
            {'results': [{'Status': 2}]},
            {'results': [{'Status': 2}]}
        ]
        invoke_data = ["1234567890"]

        action = self.get_action_instance(MOCK_CONFIG_FULL)

        action.connect = MagicMock(return_value=True)
        action.query = Mock(side_effect=query_data)
        action.invoke = MagicMock(return_value=invoke_data)

        result = action.run("router1",
                            "orion",
                            ["running", "startup"])

        self.assertEqual(result, expected)
