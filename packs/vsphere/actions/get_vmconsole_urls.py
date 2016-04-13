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

from vmwarelib.actions import BaseAction


class GetVMConsoleUrls(BaseAction):

    def run(self, vms):
        meta_url_template = 'https://{host}:{port}/vsphere-client/vmrc/vmrc.jsp?' \
                            'vm=urn:vmomi:VirtualMachine:{{vm}}:{si_uuid}'

        si_content = self.si.RetrieveContent()
        si_uuid = si_content.about.instanceUuid

        host = self.config['host']
        port = self.config['port']

        vm_url_template = meta_url_template.format(host=host, port=port, si_uuid=si_uuid)

        vm_moids = vms
        vms_console_urls = [
            {moid: {'url': vm_url_template.format(vm=moid)}} for moid in vm_moids
        ]

        return vms_console_urls
