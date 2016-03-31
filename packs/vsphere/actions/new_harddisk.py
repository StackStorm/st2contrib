import sys

from pyVmomi import vim

from vmwarelib import inventory
from vmwarelib.actions import BaseAction


class NewHardDisk(BaseAction):

    @staticmethod
    def get_backinginfo_for_existing_disk(disk_path):
        backing_info = vim.vm.device.VirtualDevice.FileBackingInfo()
        backing_info.fileName = disk_path
        return backing_info

    @staticmethod
    def get_flatfile_backinginfo(storage_format, persistence):
        backing_info = vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
        if storage_format == 'eagerzeroedthick':
            backing_info.thinProvisioned = False
            backing_info.eagerlyScrub = True
        elif storage_format == 'thin':
            backing_info.thinProvisioned = True
        elif storage_format == 'thin2gb':
            backing_info.thinProvisioned = True
            backing_info.split = True
        elif storage_format == 'thick':
            backing_info.thinProvisioned = False
        elif storage_format == 'thick2gb':
            backing_info.thinProvisioned = False
            backing_info.split = True
        backing_info.diskMode = persistence
        return backing_info

    @staticmethod
    def get_rawfile_backinginfo(device_name, persistence):
        backing_info = vim.vm.device.VirtualDisk.RawDiskMappingVer1BackingInfo()
        backing_info.deviceName = device_name
        backing_info.diskMode = persistence
        return backing_info

    @staticmethod
    def get_next_unit_number(vm):
        # See https://github.com/whereismyjetpack/pyvmomi-community-samples/blob/add-disk/samples/add_disk_to_vm.py
        unit_number = 0
        for dev in vm.config.hardware.device:
            #if hasattr(dev.backing, 'fileName'):
            if isinstance(dev, vim.VirtualDisk):
                unit_number = int(dev.unitNumber) + 1
                # unit_number 7 reserved for scsi controller
                if unit_number == 7:
                    unit_number += 1
        return unit_number

    @staticmethod
    def get_vm_reconfig_spec(vm, datastore, disk_type, storage_format, persistence, disk_path, device_name, capacity_gb):
        if disk_path:
            backing_info = NewHardDisk.get_backinginfo_for_existing_disk(disk_path)
        elif disk_type == 'flat':
            backing_info = NewHardDisk.get_flatfile_backinginfo(storage_format, persistence);
        elif disk_type.startswith('raw'):
            backing_info = NewHardDisk.get_rawfile_backinginfo(device_name, persistence);
        else:
            raise Exception("Wrong disk_type and empty disk_path. Either one should be present.")
        backing_info.datastore = datastore

        #creating Virtual Disk Device
        virtual_disk = vim.vm.device.VirtualDisk()
        virtual_disk.backing = backing_info
        virtual_disk.capacityInKB = (int(capacity_gb * 1024 * 1024) if disk_path=='' else 0)
        virtual_disk.controllerKey = 1000
        virtual_disk.unitNumber = NewHardDisk.get_next_unit_number(vm)

        #creating Virtual Device Spec
        disk_spec = vim.vm.device.VirtualDeviceSpec()
        if not disk_path:
            disk_spec.fileOperation = "create"
        disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        disk_spec.device = virtual_disk

        #creating reconfig spec
        vm_reconfig_spec = vim.vm.ConfigSpec()
        vm_reconfig_spec.deviceChange = [disk_spec]
        return vm_reconfig_spec

    @staticmethod
    def get_storage_placement_spec(ds_clust_obj, vm, vm_reconfig_spec):
        storage_placement_spec = vim.storageDrs.StoragePlacementSpec()
        storage_placement_spec.type = vim.storageDrs.StoragePlacementSpec.\
            PlacementType.reconfigure
        storage_placement_spec.configSpec = vm_reconfig_spec
        storage_placement_spec.podSelectionSpec = vim.storageDrs.PodSelectionSpec()
        storage_placement_spec.vm = vm

        vm_pod_cfg = vim.storageDrs.PodSelectionSpec.VmPodConfig()
        vm_pod_cfg.storagePod = ds_clust_obj
        disk_locator = vim.storageDrs.PodSelectionSpec.DiskLocator()
        disk_locator.diskBackingInfo = vm_reconfig_spec.deviceChange[0].device.backing
        vm_pod_cfg.disk = [disk_locator]
        storage_placement_spec.podSelectionSpec.initialVmConfig = [vm_pod_cfg]

        return storage_placement_spec

    def run(self, vms, persistence='Persistent', disk_type='flat', capacity_gb=1, datastore=None,
            datastore_cluster=None, device_name=None, disk_path='', storage_format='Thin'):
        #TODO: 'controller' parameter is missing here. The reason is because we do not support passing real objects like PowerCli
        #and there is no uuid to find and address the controller in the system.
        persistence = persistence.lower();
        disk_type = disk_type.lower();
        storage_format = storage_format.lower();

        si = self.si
        si_content = si.RetrieveContent()
        vm_objs = [vim.VirtualMachine(moid, stub=si._stub) for moid in vms]
        vm_names = [vm_obj.name for vm_obj in vm_objs] # by checking the name property, the vms' existance is checked.
        datastore_obj = None
        if datastore:
            datastore_obj = vim.Datastore(datastore, stub=si._stub)
            datastore_obj.name# by checking the name property, the vms' existance is checked.


        result=[]

        if datastore_cluster:
            ds_clust_obj = vim.StoragePod(datastore_cluster, stub=si._stub)
            ds_clust_obj.name # by retrieving the name property, the existance is checked.
            srm = si_content.storageResourceManager

            for vm in vm_objs:
                vm_reconfig_spec = NewHardDisk.get_vm_reconfig_spec(vm, datastore_obj, disk_type, storage_format, persistence, disk_path, device_name, capacity_gb)

                storage_placement_spec = NewHardDisk.get_storage_placement_spec(ds_clust_obj, vm, vm_reconfig_spec)
                datastores = srm.RecommendDatastores(storageSpec=storage_placement_spec)
                if not datastores.recommendations:
                    sys.stderr.write('Skipping the vm. There is no datastore recommendation for vm' + vm.obj._GetMoId())
                add_disk_task = srm.ApplyStorageDrsRecommendation_Task(
                    datastores.recommendations[0].key)
                successfully_added_disk = self._wait_for_task(add_disk_task)
                result.append({
                    "vm_moid":vm._GetMoId(),
                    "success":successfully_added_disk
                })
        else:
            for vm in vm_objs:
                vm_reconfig_spec = NewHardDisk.get_vm_reconfig_spec(vm, datastore_obj, disk_type, storage_format, persistence, disk_path, device_name, capacity_gb)
                add_disk_task = vm.ReconfigVM_Task(spec=vm_reconfig_spec)
                successfully_added_disk = self._wait_for_task(add_disk_task)
                result.append({
                    "vm_moid":vm._GetMoId(),
                    "success":successfully_added_disk
                })

        return result
