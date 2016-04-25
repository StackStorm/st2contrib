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


class VMCreateFromTemplate(BaseAction):

    def run(self, name, template_id, datacenter_id, resourcepool_id, datastore_id):
        # convert ids to stubs
        template = inventory.get_virtualmachine(self.si_content, template_id)
        datacenter = inventory.get_datacenter(self.si_content, datacenter_id)
        resourcepool = inventory.get_resource_pool(self.si_content, resourcepool_id)
        datastore = inventory.get_datastore(self.si_content, datastore_id)
        # prep objects for consumption
        target_folder = datacenter.vmFolder

        # relocate spec
        relocatespec = vim.vm.RelocateSpec()
        relocatespec.datastore = datastore
        relocatespec.pool = resourcepool

        # clone spec
        clonespec = vim.vm.CloneSpec()
        clonespec.location = relocatespec
        clonespec.powerOn = False
        clonespec.template = False

        task = template.CloneVM_Task(folder=target_folder, name=name, spec=clonespec)
        self._wait_for_task(task)
        if task.info.state != vim.TaskInfo.State.success:
            raise Exception(task.info.error.msg)

        return {'task_id': task._moId, 'vm_id': task.info.result._moId}
