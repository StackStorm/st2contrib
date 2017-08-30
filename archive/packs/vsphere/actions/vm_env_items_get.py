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
from pyVmomi import vim


class GetItems(BaseAction):

    def run(self, itemtype, parents=False, summary=False, vsphere=None):
        """
        Return List of items within specified Vsphere endpoint.
        Can be used to return a list or a summary of the items.

        Args:
        - itemtype: What type of object to retrieve
        - parents: Include Parent ID for hierarchy generation
        - summary: include object summary within results
        - vsphere: Which endpoint to connect to.

        Returns:
        - dict: JSON structured lits
        """
        items = {'DataCenter': vim.Datacenter,
                 'DataCenter Cluster': vim.ClusterComputeResource,
                 'Resource Pool': vim.ResourcePool,
                 'DataStore Cluster': vim.StoragePod,
                 'DataStore': vim.Datastore,
                 'Virtual Machines': vim.VirtualMachine,
                 'Networks': vim.Network,
                 'Distrubuted Portgroup': vim.DistributedVirtualPortgroup,
                 'Hosts': vim.HostSystem}

        objecttype = items[itemtype]
        results = {}
        self.establish_connection(vsphere)

        itemlist = inventory.get_managed_entities(self.si_content, objecttype)
        for item in itemlist.view:
            values = {}
            values["ID"] = str(item)
            if parents:
                values["Parent"] = str(item.parent)

            if itemtype != 'DataCenter' and summary:
                values["summary"] = str(item.summary)

            results[item.name] = values

        return results
