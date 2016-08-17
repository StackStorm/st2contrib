# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional pkg_information regarding copyright ownership.
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
# limitations under the License.

import requests
import six.moves.http_client as http_client

from st2actions.runners import pythonrunner

__all__ = [
    'ListPackagesAction'
]

BASE_URL = 'https://%(api_token)s:@packagecloud.io/api/v1/repos/%(repo)s/packages.json'
MAX_PAGE_NUMBER = 100


class ListPackagesAction(pythonrunner.Action):
    def run(self, repo, package, distro_version, version, release, api_token, per_page=200):
        params = {'per_page': per_page}
        values = {'repo': repo, 'api_token': api_token}
        url = BASE_URL % values

        page = 1
        packages = []

        while page < MAX_PAGE_NUMBER:
            page_url = url + '?page=' + str(page)
            response = requests.get(url=page_url, params=params)

            if response.status_code != http_client.OK:
                raise Exception(response.text)

            packages += response.json()

            if len(packages) >= int(response.headers.get('Total', 0)):
                break

            page += 1

        if package:
            packages = [pkg_info for pkg_info in packages if pkg_info['name'] == package]

        if distro_version:
            packages = [
                pkg_info for pkg_info in packages if pkg_info['distro_version'] == distro_version
            ]

        if version:
            packages = [pkg_info for pkg_info in packages if pkg_info['version'] == version]

        if release:
            packages = [pkg_info for pkg_info in packages if pkg_info['release'] == release]

        return sorted(packages, key=lambda x: (x['version'], x['release']), reverse=True)
