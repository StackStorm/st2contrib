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

from lib.icsp import ICSPBaseActions


class FormatServerData(ICSPBaseActions):
    def run(self, identifiers, identifier_type, hostnames,
            domains=None, workgroups=None, connection_details=None):
        if identifier_type == "mid":
            self.validate_mids(identifiers)
            mids = identifiers
        else:
            self.set_connection(connection_details)
            self.get_sessionid()
            mids = self.get_mids(identifiers, identifier_type)
        if len(mids) == len(hostnames):
            output = {}
            for i in range(len(mids)):
                values = {}
                values['hostname'] = hostnames[i]
                if domains:
                    if len(mids) == len(domains):
                        values['domain'] = domains[i]
                if workgroups:
                    if len(mids) == len(workgroups):
                        values['workgroup'] = workgroups[i]
                output[mids[i]] = values
        else:
            raise ValueError('Matched IDs and Hostname Array counts do '
                             'not match. Check identifiers and hostnames')

        return output
