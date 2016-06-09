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

from opsgenie_base_test_case import OpsGenieBaseActionTestCase

from get_schedule_who_is_on_call import ScheduleWhoIsOnCallAction


class ScheduleWhoIsOnCallTestCase(OpsGenieBaseActionTestCase):
    __test__ = True
    action_cls = ScheduleWhoIsOnCallAction

    def test_run_api_invalid_ley(self):
        action, adapter = self._get_action_status_code(
            "GET",
            "mock://api.opsgenie.com/v1/json/schedule/whoIsOnCall",
            status_code=400)
        self.assertRaises(ValueError,
                          action.run)

    def test_run_api_404(self):
        action, adapter = self._get_action_status_code(
            "GET",
            "mock://api.opsgenie.com/v1/json/schedule/whoIsOnCall",
            status_code=404)
        self.assertRaises(ValueError,
                          action.run)

    def test_run_invalid_json(self):
        action, adapter = self._get_action_invalid_json(
            "GET",
            "mock://api.opsgenie.com/v1/json/schedule/whoIsOnCall")

        self.assertRaises(ValueError,
                          action.run)

    def test_run_api_success(self):
        expected = self.load_json("schedule_whoIsOnCall.json")

        action, adapter = self._get_mocked_action()
        adapter.register_uri('GET',
                             "mock://api.opsgenie.com/v1/json/schedule/whoIsOnCall",
                             text=self.get_fixture_content("schedule_whoIsOnCall.json"))

        result = action.run()
        self.assertEqual(result, expected)
