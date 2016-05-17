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

import xml.etree.ElementTree as ET

from lib.actions import OrionBaseAction
# from lib.utils import discovery_status_to_text


class GetDiscoveryProgress(OrionBaseAction):
    def run(self, profile_id, platform):
        """
        Get the progress of a discovery profile.

        Args:
            profile_id: The id of the profile to query.
            platform: The orion platform to act on.

        Returns:
            dict: Of information from GetDiscoveryProgress Orion.Discovery
                  verb.

        Raises:
            None: Does not raise any exceptions.
        """
        results = {}

        self.connect(platform)

        orion_data = self.invoke("Orion.Discovery",
                                 "GetDiscoveryProgress",
                                 profile_id)

        root = ET.fromstring(orion_data)

        # FIXME - action disabled - this does not work as status is a nested element
        for child in root:
            key = child.tag
            results[key.replace("{http://schemas.solarwinds.com/2008/Orion}",
                                "")] = child.text
            # For Status use discovery_status_to_text to get the text.

        return results
