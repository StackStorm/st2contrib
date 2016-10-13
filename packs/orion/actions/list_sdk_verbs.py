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

import re

from lib.actions import OrionBaseAction


class ListSdkVerbs(OrionBaseAction):
    def run(self, can_invoke=True, v_filter=None):
        """
        List the Orion SDK Verbs

        Args:
            can_invoke: Limit to verbs what can be Invoked by the API.
            v_filter: Limit returned Verbs that match the filter.

        Returns:
            dict: Containing the returned data.

        Raises:
            None: Does not raise exceptions.
        """

        results = {'Entities': []}
        self.connect()

        swql = """SELECT Name, MethodName, EntityName
        FROM Metadata.Verb where CanInvoke=@CanInvoke"""
        kargs = {'CanInvoke': can_invoke}
        orion_data = self.query(swql, **kargs)

        if v_filter is not None:
            m = re.compile("{}".format(v_filter))

        for item in orion_data['results']:
            if v_filter is not None:
                if m.search(
                        item['EntityName']) or m.search(item['MethodName']):
                    pass
                else:
                    continue

            results['Entities'].append({'Entity': item['EntityName'],
                                        'Method': item['MethodName']})
        return results
