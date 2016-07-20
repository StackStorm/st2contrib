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
# limitations under the License.

from lib.actions import CloudflareBaseAction


class GetIPsAction(CloudflareBaseAction):
    def run(self):
        """
        Get CloudFlare IPs

        Args:
            None.

        Raises:
            ValueError: On HTTP Error or Invaild JSON.
            requests.exceptions.MissingSchema: If https:// missing from
                                               api_host.
            Exception: On "success": false from API.

        Returns:
            dict: containing 'ipv4_cidrs' and 'ipv6_cidrs'
        """

        results = {}

        url = "{}/client/v4/ips".format(self.API_HOST)
        payload = {}
        headers = {"Content-Type": "application/json"}

        data = self._get(url, headers, payload)

        if data['success'] is True:
            results['messages'] = data['messages']
            results['ipv4_cidrs'] = data['result']['ipv4_cidrs']
            results['ipv6_cidrs'] = data['result']['ipv6_cidrs']

            return results
        else:
            for error in data['errors']:
                self.send_user_error(error)

            raise Exception("Error from Cloudflare: {}".format(data['errors']))
