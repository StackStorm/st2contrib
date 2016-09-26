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

import time
import datetime

from lib.base import BaseGithubAction


class GetDeploymentStatusesAction(BaseGithubAction):
    def run(self, api_user, repository, deployment_id, github_type):

        enterprise = self._is_enterprise(github_type)

        if api_user:
            self.token = self._get_user_token(api_user, enterprise)

        payload = {"id": deployment_id}

        responses = self._request("GET",
                                  "/repos/{}/deployments/{}/statuses".format(
                                      repository, deployment_id),
                                  payload,
                                  self.token,
                                  enterprise)

        results = []
        for response in responses:
            ts_created_at = time.mktime(
                datetime.datetime.strptime(
                    response['created_at'],
                    "%Y-%m-%dT%H:%M:%SZ").timetuple())

            results.append({'creator': response['creator']['login'],
                            'id': response['id'],
                            'description': response['description'],
                            'state': response['state'],
                            'target_url': response['target_url'],
                            'created_at': response['created_at'],
                            'updated_at': response['updated_at'],
                            'ts_created_at': ts_created_at})

        return results
