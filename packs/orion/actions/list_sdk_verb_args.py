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

from lib.actions import OrionBaseAction


class ListSdkVerbArgs(OrionBaseAction):
    def run(self, platform, entity_name, verb_name):
        """
        List the Orion SDK Verbs

        Args:
            platform: The orion platform to act on.
            entity_name: The EntityName to query.
            verb_name: The VerbName to query.

        Returns:
            dict: Of a verb's args taken from the Orion DB.

        Raises:
            None: Does not raise any exceptions.
        """

        results = {'verb_arguments': []}
        self.connect(platform)

        swql = """SELECT EntityName, VerbName, Position, Name, Type,
        XmlTemplate, XmlSchemas, IsOptional
        FROM Metadata.VerbArgument WHERE EntityName=@EntityName
        and VerbName=@VerbName
        ORDER BY Position"""
        kargs = {'EntityName': entity_name,
                 'VerbName': verb_name}
        orion_data = self.query(swql, **kargs)

        for item in orion_data['results']:
            results['verb_arguments'].append(
                {'position': item['Position'],
                 'name': item['Name'],
                 'type': item['Type'],
                 'optional': item['IsOptional']})
        return results
