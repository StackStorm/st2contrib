from pyVmomi import vim


def get_managed_entity(content, vimtype, moid=None, name=None):
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vimtype], True)
    for entity in container.view:
        # verify if this works.
        if moid and entity._moId == moid:
            return entity
        elif name and entity.name == name:
            return entity

    #if this area is reached no object has been found
    #if no arguments were passed just return with empty object
    if ((name is None or name == "") and (moid is None or moid == "")):
        return
    #if a name was passed error
    elif (name is not None and name != ""):
        raise Exception("Inventory Error: Unable to Find Object (%s): %s"
                        % (vimtype, name))
    #if a moid was passed error
    elif (moid is not None and moid != ""):
        raise Exception("Inventory Error: Unable to Find Object (%s): %s"
                        % (vimtype, moid))
    #catch all error
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


def get_virtualmachine(content, moid=None, name=None):
    return get_managed_entity(content, vim.VirtualMachine,
                              moid=moid, name=name)


def get_virtualmachines(content):
    return get_managed_entities(content, vim.VirtualMachine)


def get_task(content, moid=None):
    return get_managed_entity(content, vim.Task,
                              moid=moid, name=None)
