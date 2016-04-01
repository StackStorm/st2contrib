from pyVmomi import vim

from vmwarelib.actions import BaseAction


class GetVMs(BaseAction):

    def run(self, ids=None, names=None, datastores=None, datastore_clusters=None,
            resource_pools=None, vapps=None, hosts=None, folders=None, clusters=None,
            datacenters=None, virtual_switches=None, no_recursion=False):
        # TODO: food for thought. PowerCli contains additional parameters that are not present
        # here for the folliwing reason:
        # <server> - we may need to bring it in if we decide to have connections to more than 1 VC.
        # <tag>    - Tags in VC are not the same as tags you see in Web Client for the reason, that
        #            those tags are stored in Inventory Service only. PowerCli somehow can access
        #            it, from vSphere SDK there is no way.

        si = self.si
        si_content = si.RetrieveContent()
        props = ['name', 'runtime.powerState']
        moid_to_vm = {}

        # getting vms by their ids
        vms_from_vmids = []
        if ids:
            vms_from_vmids = [vim.VirtualMachine(moid, stub=si._stub) for moid in ids]
            GetVMs.__add_vm_properties_to_map_from_vm_array(moid_to_vm, vms_from_vmids)

        # getting vms by their names
        vms_from_names = []
        if names:
            container = si_content.viewManager.CreateContainerView(si_content.rootFolder,
                                                                   [vim.VirtualMachine], True)
            for vm in container.view:
                if vm.name in names:
                    vms_from_names.append(vm)
            GetVMs.__add_vm_properties_to_map_from_vm_array(moid_to_vm, vms_from_names)

        # getting vms from datastore objects
        vms_from_datastores = []
        if datastores:
            vim_datastores = [vim.Datastore(moid, stub=si._stub) for moid in datastores]
            for ds in vim_datastores:
                vms_from_datastores.extend(ds.vm)
            GetVMs.__add_vm_properties_to_map_from_vm_array(moid_to_vm, vms_from_datastores)

        # getting vms from datastore cluster objects
        vms_from_datastore_clusters = []
        if datastore_clusters:
            vim_datastore_clusters = [
                vim.StoragePod(moid, stub=si._stub) for moid in datastore_clusters
            ]
            for ds_cl in vim_datastore_clusters:
                for ds in ds_cl.childEntity:
                    vms_from_datastore_clusters.extend(ds.vm)
            GetVMs.__add_vm_properties_to_map_from_vm_array(moid_to_vm,
                vms_from_datastore_clusters)

        # getting vms from virtual switch objects
        vms_from_virtual_switches = []
        if virtual_switches:
            vim_virtual_switches = [
                vim.DistributedVirtualSwitch(moid, stub=si._stub) for moid in virtual_switches
            ]
            for vswitch in vim_virtual_switches:
                for pg in vswitch.portgroup:
                    vms_from_virtual_switches.extend(pg.vm)
            GetVMs.__add_vm_properties_to_map_from_vm_array(moid_to_vm, vms_from_virtual_switches)

        # getting vms from containers (location param)
        vms_from_containers = []
        containers = []

        if resource_pools:
            containers += [vim.ResourcePool(moid, stub=si._stub) for moid in resource_pools]

        if vapps:
            containers += [vim.VirtualApp(moid, stub=si._stub) for moid in vapps]

        if hosts:
            containers += [vim.HostSystem(moid, stub=si._stub) for moid in hosts]

        if folders:
            containers += [vim.Folder(moid, stub=si._stub) for moid in folders]

        if clusters:
            containers += [vim.ComputeResource(moid, stub=si._stub) for moid in clusters]

        if datacenters:
            containers += [vim.Datacenter(moid, stub=si._stub) for moid in datacenters]

        for cont in containers:
            objView = si_content.viewManager.CreateContainerView(cont, [vim.VirtualMachine],
                not no_recursion)
            tSpec = vim.PropertyCollector.TraversalSpec(name='tSpecName', path='view', skip=False,
                type=vim.view.ContainerView)
            pSpec = vim.PropertyCollector.PropertySpec(all=False, pathSet=props,
                type=vim.VirtualMachine)
            oSpec = vim.PropertyCollector.ObjectSpec(obj=objView, selectSet=[tSpec], skip=False)
            pfSpec = vim.PropertyCollector.FilterSpec(objectSet=[oSpec], propSet=[pSpec],
                reportMissingObjectsInResults=False)
            retOptions = vim.PropertyCollector.RetrieveOptions()
            retProps = si_content.propertyCollector.RetrievePropertiesEx(specSet=[pfSpec],
                options=retOptions)
            vms_from_containers += retProps.objects
            while retProps.token:
                retProps = si_content.propertyCollector.ContinueRetrievePropertiesEx(
                    token=retProps.token)
                vms_from_containers += retProps.objects
            objView.Destroy()

        for vm in vms_from_containers:
            if vm.obj._GetMoId() not in moid_to_vm:
                moid_to_vm[vm.obj._GetMoId()] = {
                    "moid": vm.obj._GetMoId(),
                    "name": vm.propSet[0].val,
                    "runtime.powerState": vm.propSet[1].val
                }

        return moid_to_vm.values()

    @staticmethod
    def __add_vm_properties_to_map_from_vm_array(vm_map, vm_array):
        for vm in vm_array:
            if vm._GetMoId() not in vm_map:
                vm_map[vm._GetMoId()] = {
                    "moid": vm._GetMoId(),
                    "name": vm.name,
                    "runtime.powerState": vm.runtime.powerState
                }
