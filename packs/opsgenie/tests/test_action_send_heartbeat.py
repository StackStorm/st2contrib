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

import requests_mock

from opsgenie_base_test_case import OpsGenieBaseActionTestCase

from send_heartbeat import SendHeartbeatAction

class SendHeartbeatTestCase(OpsGenieBaseActionTestCase):
    __test__ = True
    action_cls = SendHeartbeatAction

    def test_run_api_404(self):
        action = self.get_action_instance(self.full_config)

        adapter = requests_mock.Adapter()
        action.session.mount('mock', adapter)
        adapter.register_uri('POST',
                             "mock://api.opsgenie.com/v1/json/heartbeat/send",
                             status_code=404)

        self.assertRaises(ValueError,
                          action.run,
                          "Test")

    def test_run_invalid_json(self):
        action = self.get_action_instance(self.full_config)

        adapter = requests_mock.Adapter()
        action.session.mount('mock', adapter)
        adapter.register_uri('POST',
                             "mock://api.opsgenie.com/v1/json/heartbeat/send",
                             text="{'ffo': bar}")

        self.assertRaises(ValueError,
                          action.run,
                          "Test")

    def test_run_api_success(self):
        expected = self.load_json("send_heartbeat.json")

        action = self.get_action_instance(self.full_config)

        adapter = requests_mock.Adapter()
        action.session.mount('mock', adapter)
        adapter.register_uri('POST',
                             "mock://api.opsgenie.com/v1/json/heartbeat/send",
                             text=self.get_fixture_content("send_heartbeat.json"))

        result = action.run("Test")
        self.assertEqual(result, expected)
