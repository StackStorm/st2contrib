from pyVmomi import vim


def get_managed_entity(content, vimtype, moid=None, name=None):
    container = content.viewManager.CreateContainerView(content.rootFolder, [vimtype], True)
    for entity in container.view:
        # verify if this works.
        if moid and entity._moId == moid:
            return entity
        elif name and entity.name == name:
            return entity


def get_datacenter(content, moid=None, name=None):
    return get_managed_entity(content, vim.Datacenter, moid=moid, name=name)


def get_folder(content, moid=None, name=None):
    return get_managed_entity(content, vim.Folder, moid=moid, name=name)


def get_resource_pool(content, moid=None, name=None):
    return get_managed_entity(content, vim.ResourcePool, moid=moid, name=name)


def get_datastore(content, moid=None, name=None):
    return get_managed_entity(content, vim.Datastore, moid=moid, name=name)


def get_network(content, moid=None, name=None):
    return get_managed_entity(content, vim.Network, moid=moid, name=name)


def get_virtualmachine(content, moid=None, name=None):
    return get_managed_entity(content, vim.VirtualMachine, moid=moid, name=name)


def get_task(content, moid=None):
    return get_managed_entity(content, vim.Task, moid=moid, name=None)
