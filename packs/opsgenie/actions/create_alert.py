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


class CreateAlertAction(OpsGenieBaseAction):
    def run(self, message, teams=None, alias=None,
            description=None, recipients=None, actions=None,
            source="StackStorm", tags=None, details=None,
            entity=None, user=None, note=None):
        """
        """

        if len(message) > 130:
            raise ValueError("Message length ({}) is over 130 chars".format(
                len(message)))

        body = {"apiKey": self.api_key,
                "message": message}

        if teams:
            body["teams"] = teams

        if alias:
            body["alias"] = alias

        if description:
            if len(description) > 15000:
                raise ValueError("Description is too long, can't be over 15000 chars")
            else:
                body["description"] = description

        if recipients:
            body["recipients"] = recipients

        if actions:
            body["actions"] = actions

        if source:
            body["source"] = source

        if tags:
            body["tags"] = tags

        if details:
            body["details"] = details

        if entity:
            body["entity"] = entity

        if user:
            body['user'] = user

        if note:
            body['note'] = note

        data = self._req("POST",
                         "v1/json/alert",
                         body=body)

        return data
