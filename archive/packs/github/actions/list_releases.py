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


class ListReleasesAction(BaseGithubAction):
    def run(self, api_user, repository, github_type):
        results = []

        enterprise = self._is_enterprise(github_type)

        if api_user:
            self.token = self._get_user_token(api_user, enterprise)

        releases = self._request("GET",
                                 "/repos/{}/releases".format(repository),
                                 None,
                                 self.token,
                                 enterprise=enterprise)

        for release in releases:
            results.append(
                {'author': release['author']['login'],
                 'html_url': release['html_url'],
                 'tag_name': release['tag_name'],
                 'target_commitish': release['target_commitish'],
                 'name': release['name'],
                 'body': release['body'],
                 'draft': release['draft'],
                 'prerelease': release['prerelease'],
                 'created_at': release['created_at'],
                 'published_at': release['published_at'],
                 'total_assets': len(release['assets'])})

        return results
