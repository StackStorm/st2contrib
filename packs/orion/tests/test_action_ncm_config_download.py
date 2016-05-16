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


class NcmConfigDownloadTestCase(BaseActionTestCase):
    action_cls = NcmConfigDownload

    def test_run_no_config(self):
        self.assertRaises(ValueError,
                          NcmConfigDownload,
                          yaml.safe_load(
                              self.get_fixture_content('blank.yaml')))

    def test_run_basic_config(self):
        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        self.assertIsInstance(action, NcmConfigDownload)

    def test_run_connect_fail(self):
        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        action.connect = Mock(side_effect=ValueError(
            'Orion host details not in the config.yaml'))

        self.assertRaises(ValueError,
                          action.run,
                          "router1",
                          "orion",
                          ["running", "startup"])

    def test_run_ncm_node_not_found(self):
        orion_data = {'results': []}

        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        action.connect = MagicMock(return_value=True)

        action.query = MagicMock(return_value=orion_data)

        self.assertRaises(Exception,
                          action.run,
                          "router1",
                          "orion",
                          ["running", "startup"])

    def test_run_ncm_download_complete(self):
        expected = {'running': {'DeviceOutput': None,
                                'ErrorMessage': None,
                                'RequestedReboot': False,
                                'RequestedScript': None,
                                'UserName': 'hubot',
                                'status': 'Complete'},
                    'startup': {'DeviceOutput': None,
                                'ErrorMessage': None,
                                'RequestedReboot': False,
                                'RequestedScript': None,
                                'UserName': 'hubot',
                                'status': 'Complete'},
                    }

        query_data = []
        query_data.append(yaml.safe_load(
            self.get_fixture_content("orion_npm_results.yaml")))
        query_data.append(yaml.safe_load(
            self.get_fixture_content("orion_ncm_results.yaml")))
        query_data.append({'results': [{"Status": 2,
                                        "UserName": "hubot",
                                        "DeviceOutput": None,
                                        "ErrorMessage": None,
                                        "RequestedScript": None,
                                        "RequestedReboot": False}]})
        query_data.append({'results': [{"Status": 2,
                                        "UserName": "hubot",
                                        "DeviceOutput": None,
                                        "ErrorMessage": None,
                                        "RequestedScript": None,
                                        "RequestedReboot": False}]})
        invoke_data = ["1234567890"]

        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        action.connect = MagicMock(return_value=True)
        action.query = Mock(side_effect=query_data)
        action.invoke = MagicMock(return_value=invoke_data)

        result = action.run("router1",
                            "orion",
                            ["running", "startup"])

        self.assertEqual(result, expected)
