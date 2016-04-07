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
from vmwarelib import checkinputs
from vmwarelib.actions import BaseAction


class VMCPUMemEdit(BaseAction):

    def run(self, vm_id, vm_name, cpu_edit, mem_edit):
        # check a means of finding the VM has been provided
        checkinputs.one_of_two_strings(vm_id, vm_name, "ID or Name")

        vm = inventory.get_virtualmachine(self.si_content,
                                          moid=vm_id,
                                          name=vm_name)
        spec = vim.vm.ConfigSpec()
        if cpu_edit:
            spec.numCPUs = cpu_edit
        if mem_edit:
            spec.memoryMB = mem_edit * 1024

        task = vm.ReconfigVM_Task(spec)
        self._wait_for_task(task)

        return {'state': str(task.info.state)}
