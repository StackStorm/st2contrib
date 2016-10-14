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


def get_managed_entity(content, vimtype, moid=None, name=None):
    if not name and not moid:
        return
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vimtype], True)
    count = 0
    for entity in container.view:
        # Find matches in the results
        if moid and entity._moId == moid:
            results = entity
            count += 1
        elif name and entity.name == name:
            results = entity
            count += 1
        # check to see if multiple matches were found
        if count >= 2:
            raise Exception("Multiple Managed Objects found,\
                            Check Names or IDs provided are unique")
        elif count == 1:
            # Single Match found
            return results

    # if this area is reached no object has been found
    # if a name was passed error
    if name:
        raise Exception("Inventory Error: Unable to Find Object (%s): %s"
                        % (vimtype, name))
    # if a moid was passed error
    elif moid:
        raise Exception("Inventory Error: Unable to Find Object (%s): %s"
                        % (vimtype, moid))
    # catch all error
    else:
        raise Exception("Inventory Error: No Name or moid provided (%s)"
                        % vimtype)


def get_managed_entities(content, vimtype):
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vimtype], True)
    return container


def get_datacenter(content, moid=None, name=None):
    return get_managed_entity(content, vim.Datacenter, moid=moid, name=name)


def get_cluster(content, moid=None, name=None):
    return get_managed_entity(content, vim.ClusterComputeResource,
                              moid=moid, name=name)


def get_folder(content, moid=None, name=None):
    return get_managed_entity(content, vim.Folder,
                              moid=moid, name=name)


def get_resource_pool(content, moid=None, name=None):
    return get_managed_entity(content, vim.ResourcePool,
                              moid=moid, name=name)


def get_datastore_cluster(content, moid=None, name=None):
    return get_managed_entity(content, vim.StoragePod,
                              moid=moid, name=name)


def get_datastore(content, moid=None, name=None):
    return get_managed_entity(content, vim.Datastore,
                              moid=moid, name=name)


def get_network(content, moid=None, name=None):
    return get_managed_entity(content, vim.Network,
                              moid=moid, name=name)


def get_distributedportgroup(content, moid=None, name=None):
    return get_managed_entity(content, vim.dvs.DistributedVirtualPortgroup,
                              moid=moid, name=name)


def get_virtualmachine(content, moid=None, name=None):
    return get_managed_entity(content, vim.VirtualMachine,
                              moid=moid, name=name)


def get_virtualmachines(content):
    return get_managed_entities(content, vim.VirtualMachine)


def get_task(content, moid=None):
    return get_managed_entity(content, vim.Task,
                              moid=moid, name=None)
