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

from pyVmomi import vim

from vmwarelib import inventory
from vmwarelib.actions import BaseAction


class VMRemove(BaseAction):

    def run(self, vm_id, delete_permanently, vsphere=None):
        """
        Remove virtual machine from vsphere

        Args:
        - vm_id: Moid of Virtual Machine to edit
        - vm_name: Name of Virtual Machine to edit
        - vsphere: Pre-configured vsphere connection details (config.yaml)
        - delete_permenantly: Delete files as well as unregister from vsphere

        Returns:
        - dict: success: true/false
        """

        self.establish_connection(vsphere)

        vm = inventory.get_virtualmachine(self.si_content, moid=vm_id)

        if vm.runtime.powerState == vim.VirtualMachine.PowerState.poweredOn:
            raise Exception("VM Currently Powered On")
        if delete_permanently:
            task = vm.Destroy_Task()
            success = self._wait_for_task(task)
        else:
            vm.UnregisterVM()
            success = True

        return {"success": success}
