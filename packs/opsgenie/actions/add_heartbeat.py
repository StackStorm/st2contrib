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

from lib.actions import OpsGenieBaseAction


class AddHeartbeatAction(OpsGenieBaseAction):
    def run(self, name, interval=None, interval_unit=None, description=None, enabled=False):
        """
        Add a Heartbeat to OpsGenie

        Args:
        - name: Name of the heartbeat
        - interval: Specifies how often a heartbeat message should be expected.
        - intervalUnit: interval specified as minutes, hours or days.
        - description: An optional description of the heartbeat.
        - enabled: Enable/disable heartbeat monitoring.

        Returns:
        - dict: Data from OpsGenie
        """

        body = {"apiKey": self.api_key,
                "name": name,
                "enabled": enabled}

        if interval:
            body["interval"] = interval

        if interval_unit:
            body["intervalUnit"] = interval_unit

        if description:
            body["description"] = description

        data = self._req("POST",
                         "v1/json/heartbeat",
                         body=body)

        return data
