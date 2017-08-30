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


class VMCreateBareBones(BaseAction):
    def run(self, vm_name, cluster, datastore_cluster,
            datastore, resourcepool, cpu_size, ram_size,
            guestos, version, description, vsphere=None):
        """
        Create barebones VM (CPU/RAM/Graphics)

        Args:
        - vm_name: Name of Virtual Machine to create
        - vsphere: Pre-configured vsphere connection details (config.yaml)
        - description: Short Description of VM and it's purpose
        - cpu_size: Number of vCPUs to allocate
        - ram_size: Ammount of memory to assign (GB)
        - datastore_cluster: name of DataStore Cluster to use for VM Files
        - datastore: Individual datastore to put vm files within.
                     Not needed if datastore_cluster is set
        - cluster: Cluster within vsphere to host virtual machine
        - version: VM version to set
        - guestos: Code for GuestOS that will be installed on this VM
        - resourepool: vsphere resource pool to assign new VM to

        Returns:
        - dict: vm moid of newly created vm
        """
        # Setup Identifiers for objects
        self.establish_connection(vsphere)
        si = self.si
        si_content = si.RetrieveContent()
        # checkinputs.vm_storage(datastore_cluster, datastore)
        checkinputs.one_of_two_strings(datastore_cluster,
                                       datastore,
                                       "Datastore Cluster or Datastore")

        data_center = self.si_content.rootFolder.childEntity[0]
        cluster = inventory.get_cluster(self.si_content, name=cluster)
        data_store_cluster = inventory.get_datastore_cluster(
            self.si_content,
            name=datastore_cluster)
        # data_store = inventory.get_datastore(self.si_content, name=datastore)
        target_folder = data_center.vmFolder

        # If No Resource Pool issued the Default one for
        # the Cluster will be selected.
        if resourcepool:
            resource_pool = inventory.get_resource_pool(self.si_content,
                                                        name=resourcepool)
        else:
            resource_pool = cluster.resourcePool

        # Config created that is required for DS selection
        # Config is BareBones, CPU RAM no more.
        config = vim.vm.ConfigSpec(name=vm_name,
                                   memoryMB=(ram_size * 1024),
                                   numCPUs=cpu_size,
                                   guestId=guestos,
                                   version=version,
                                   cpuHotAddEnabled=True,
                                   memoryHotAddEnabled=True,
                                   annotation=description)

        # if Datastore cluster is provided it will find the
        # recommended Datastore to store VM files
        if datastore_cluster:
            podsel = vim.storageDrs.PodSelectionSpec()
            podsel.storagePod = data_store_cluster

            storage_spec = vim.storageDrs.StoragePlacementSpec(
                type='create',
                configSpec=config,
                resourcePool=resource_pool,
                podSelectionSpec=podsel,
                folder=target_folder)

            # Create Instance of Storage Resource Manager -
            # This is used to identify a Recommended Datastore from a Cluster
            srm = si_content.storageResourceManager
            results = srm.RecommendDatastores(storageSpec=storage_spec)
            rec_ds = results.recommendations[0].action[0]\
                .relocateSpec.datastore
            datastore_path = '[' + rec_ds.name + '] ' + vm_name
        else:
            # No Datastore Cluster has been offered so using the D
            if datastore:
                datastore_path = '[' + datastore + '] ' + vm_name
            else:
                raise Exception('Error No Storage Data Provided')

        # Now Datastore is known the remaining
        # of VM Config can be setup and added
        vmx_file = vim.vm.FileInfo(logDirectory=None,
                                   snapshotDirectory=None,
                                   suspendDirectory=None,
                                   vmPathName=datastore_path)
        config.files = vmx_file

        # Create task to Build actual Machine
        task = target_folder.CreateVM_Task(config=config, pool=resource_pool)
        self._wait_for_task(task)
        if task.info.state != vim.TaskInfo.State.success:
            raise Exception(task.info.error.msg)

        return {'vm_id': task.info.result._moId}
