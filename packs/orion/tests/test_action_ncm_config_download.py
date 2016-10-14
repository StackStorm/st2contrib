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

from ncm_config_download import NcmConfigDownload

__all__ = [
    'NcmConfigDownloadTestCase'
]


class NcmConfigDownloadTestCase(OrionBaseActionTestCase):
    __test__ = True
    action_cls = NcmConfigDownload

    def test_run_connect_fail(self):
        action = self.setup_connect_fail()
        self.assertRaises(ValueError,
                          action.run,
                          "router1",
                          ["running", "startup"])

    def test_run_ncm_node_not_found(self):
        action = self.setup_query_blank_results()
        self.assertRaises(Exception,
                          action.run,
                          "router1",
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
        query_data.append(self.query_npm_node)
        query_data.append(self.query_ncm_node)
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

        action = self.get_action_instance(config=self.full_config)

        action.connect = MagicMock(return_value="orion")
        action.query = MagicMock(side_effect=query_data)
        action.invoke = MagicMock(return_value=invoke_data)

        result = action.run("router1",
                            ["running", "startup"])

        self.assertEqual(result, expected)
