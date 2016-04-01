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

import eventlet

from pyVmomi import vim

from vmwarelib import inventory
from vmwarelib.actions import BaseAction


class VMCheckTools(BaseAction):

    def run(self, vm_id):
        # convert ids to stubs
        vm = inventory.get_virtualmachine(self.si_content, moid=vm_id)

        # To correctly understand tools status need to consult 3 properties
        # 'powerState' 'ttoolsVersionStatus2' and 'toolsRunningStatus'

        # If VM isn't powered on tools state is meaningless.
        if vm.runtime.powerState != vim.VirtualMachine.PowerState.poweredOn:
            return {"status": vm.runtime.powerState}

        # Tools not installed.
        if vm.guest.toolsVersionStatus2 == \
           vim.vm.GuestInfo.ToolsVersionStatus.guestToolsNotInstalled:
            return {"status": vm.guest.toolsVersionStatus2}

        # Scripts still running therefore wait.
        while vm.guest.toolsRunningStatus != \
                vim.vm.GuestInfo.ToolsRunningStatus.guestToolsRunning:
            eventlet.sleep(1)

        # verify status is running.
        return {"status": vm.guest.toolsRunningStatus}
