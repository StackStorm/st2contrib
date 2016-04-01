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

from vmwarelib.actions import BaseAction


class SetVM(BaseAction):
    def run(self, vm, alternate_guest_name=None, description=None, guest_id=None, memory_mb=None,
            name=None, num_cpu=None, vm_swapfile_policy=None):
        vm_swapfile_policy = vm_swapfile_policy.lower() if vm_swapfile_policy else None

        si = self.si

        vm_obj = vim.VirtualMachine(vm, stub=si._stub)

        # convert ids to stubs
        spec = vim.vm.ConfigSpec()
        spec.alternateGuestName = alternate_guest_name
        spec.annotation = description
        spec.guestId = guest_id
        spec.memoryMB = memory_mb
        spec.name = name
        spec.numCPUs = num_cpu
        if vm_swapfile_policy == 'inhostdatastore':
            spec.swapPlacement = 'hostLocal'
        elif vm_swapfile_policy == 'withvm':
            spec.swapPlacement = 'vmDirectory'

        task = vm_obj.ReconfigVM_Task(spec)

        success = self._wait_for_task(task)

        return {'success': success}
