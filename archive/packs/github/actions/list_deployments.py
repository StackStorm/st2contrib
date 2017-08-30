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


class ListDeploymentsAction(BaseGithubAction):
    def run(self, api_user, repository, github_type):
        results = []

        enterprise = self._is_enterprise(github_type)

        if api_user:
            self.token = self._get_user_token(api_user,
                                              enterprise)

        response = self._request("GET",
                                 "/repos/{}/deployments".format(repository),
                                 None,
                                 self.token,
                                 enterprise)

        for dep in response:
            results.append(
                {'creator': dep['creator']['login'],
                 'statuses_url': dep['statuses_url'],
                 'repository_url': dep['repository_url'],
                 'ref': dep['ref'],
                 'task': dep['task'],
                 'payload': dep['payload'],
                 'environment': dep['environment'],
                 'description': dep['description'],
                 'created_at': dep['created_at'],
                 'updated_at': dep['updated_at']})

        return results
