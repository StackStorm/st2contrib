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
import sys

from vmwarelib import inventory
from vmwarelib import checkinputs
from vmwarelib.actions import BaseAction


class VMAddHDD(BaseAction):
    def run(self, vm_id, vm_name, datastore_cluster,
            datastore, disk_size, provision_type):
        # ensure that minimal inputs are provided
        checkinputs.one_of_two_strings(vm_id, vm_name, "ID or Name")

        vm = inventory.get_virtualmachine(self.si_content, vm_id, vm_name)
        spec = vim.vm.ConfigSpec()
        hdd_unit_number = self.get_next_unit_number(vm)
        ctrl_key = self.get_controller_key(vm)

        # Prepare new Disk configuration
        disk_changes = []
        disk_spec = vim.vm.device.VirtualDeviceSpec()
        disk_spec.fileOperation = "create"
        disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        disk_spec.device = vim.vm.device.VirtualDisk()
        disk_spec.device.backing =\
            vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
        disk_spec.device.backing.diskMode = "persistent"

        if provision_type == 'thin':
            disk_spec.device.backing.thinProvisioned = True

        disk_spec.device.unitNumber = hdd_unit_number
        disk_spec.device.capacityInKB = int(disk_size) * 1024 * 1024
        disk_spec.device.controllerKey = ctrl_key

        # If Datastore Cluster is provided attach Disk via that
        if datastore_cluster:
            ds_clust_obj = inventory.get_datastore_cluster(
                self.si_content, name=datastore_cluster)
            disk_changes.append(disk_spec)
            spec.deviceChange = disk_changes
            srm = self.si_content.storageResourceManager

            storage_placement_spec = self.get_storage_placement_spec(
                ds_clust_obj, vm, spec)
            datastores = srm.RecommendDatastores(
                storageSpec=storage_placement_spec)

            if not datastores.recommendations:
                sys.stderr.write('Skipping as No datastore Recommendations')

            add_disk_task = srm.ApplyStorageDrsRecommendation_Task(
                datastores.recommendations[0].key)

        elif datastore:
            datastore_obj = inventory.get_datastore(self.si_content,
                                                    name=datastore)
            disk_spec.device.backing.datastore = datastore_obj
            disk_changes.append(disk_spec)
            spec.deviceChange = disk_changes
            add_disk_task = vm.ReconfigVM_Task(spec)
        else:
            disk_changes.append(disk_spec)
            spec.deviceChange = disk_changes
            add_disk_task = vm.ReconfigVM_Task(spec)

        successfully_added_disk = self._wait_for_task(add_disk_task)
        return {'state': successfully_added_disk}

    def get_storage_placement_spec(self, ds_clust_obj, vm, vm_reconfig_spec):
        storage_placement_spec = vim.storageDrs.StoragePlacementSpec()
        storage_placement_spec.type =\
            vim.storageDrs.StoragePlacementSpec.PlacementType.reconfigure
        storage_placement_spec.configSpec = vm_reconfig_spec
        storage_placement_spec.podSelectionSpec =\
            vim.storageDrs.PodSelectionSpec()
        storage_placement_spec.vm = vm

        vm_pod_cfg = vim.storageDrs.PodSelectionSpec.VmPodConfig()
        vm_pod_cfg.storagePod = ds_clust_obj
        disk_locator = vim.storageDrs.PodSelectionSpec.DiskLocator()
        disk_locator.diskBackingInfo =\
            vm_reconfig_spec.deviceChange[0].device.backing
        vm_pod_cfg.disk = [disk_locator]
        storage_placement_spec.podSelectionSpec.initialVmConfig = [vm_pod_cfg]
        return storage_placement_spec

    def get_next_unit_number(self, vm):
        unit_number = 0
        # Cycle though devices on VM and find
        # entries with attribute "fileName".
        for device in vm.config.hardware.device:
            if hasattr(device.backing, 'fileName'):
                unit_number = int(device.unitNumber) + 1
                # unit number 7 is reserved
                if unit_number == 7:
                    unit_number += 1
        return unit_number

    def get_controller_key(self, vm):
        # 1000 is the default used for hdd controllers
        key = 1000
        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualSCSIController):
                key = device.key
        return key
