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


class CloseAlertAction(OpsGenieBaseAction):
    def run(self, alert_id=None, alias=None, user=None, note=None, source="StackStorm"):
        """
        Close alert request is used to close open alerts in OpsGenie.

        Args:
        - alert_id: Id of the alert that will be closed.
        - alias: Alias of the alert that will be closed.
        - user: Default owner of the execution.
        - note: Additional alert note
        - source: User defined field to specify source of close action.

        Returns:
        - dict: Data from OpsGenie

        Raises:
        - ValueError: If alias and alert_id are None.
        """

        body = {"apiKey": self.api_key,
                "source": source}

        if alias:
            body["alias"] = alias
        elif alert_id:
            body["id"] = alert_id
        else:
            raise ValueError("Need one of alias or alert_id to be set.")

        if user:
            body['user'] = user

        if note:
            body['note'] = note

        data = self._req("POST",
                         "v1/json/alert/close",
                         body=body)

        return data
