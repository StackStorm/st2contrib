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

from vmwarelib import inventory
from vmwarelib.actions import BaseAction


class GetVMMoid(BaseAction):

    def run(self, vm_names, vsphere=None):
        """
        Return moid values for VMs listed within the vsphere.

        Args:
        - vm_names: list of names as shown in vsphere

        Returns:
        - dict: key value pair of vm_name and vm moid.
        """

        results = {}
        self.establish_connection(vsphere)

        vmlist = inventory.get_virtualmachines(self.si_content)

        for vm in vmlist.view:
            if vm_names:
                if vm.name in vm_names:
                    results[vm.name] = str(vm).split(':')[-1].replace("'", "")
            else:
                results[vm.name] = str(vm).split(':')[-1].replace("'", "")

        return results
