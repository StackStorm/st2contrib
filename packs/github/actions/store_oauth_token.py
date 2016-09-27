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

from lib.base import BaseGithubAction


class StoreOauthTokenAction(BaseGithubAction):
    def run(self, user, token, github_type):
        enterprise = self._is_enterprise(github_type)

        if enterprise:
            value_name = "token_enterprise_{}".format(user)
            results = {'github_type': "enterprise"}
        else:
            value_name = "token_{}".format(user)
            results = {'github_type': "online"}

        self.action_service.set_value(
            name=value_name,
            value=token)

        return results
