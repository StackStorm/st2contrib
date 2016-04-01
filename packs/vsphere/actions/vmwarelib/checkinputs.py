def vm_identifier(moid=None, name=None):
    if ((name is None or name == "")
            and (moid is None or moid == "")):
        raise Exception("No VM Name or Object ID provided")


def vm_storage(datastorecluster=None, datastore=None):
    if ((datastorecluster is None or datastorecluster == "")
            and (datastore is None or datastore == "")):
        raise Exception("Niether Datastore Cluster nor Datastore provided.")
