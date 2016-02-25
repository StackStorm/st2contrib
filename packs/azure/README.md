# Microsoft Azure Integration Pack

Pack which contains integrations for different Microsoft Azure services.

## Configuration

* ``compute.subscription_id`` - Your Azure subscription ID.
* ``compute.cert_file`` - Path to the certificate file used for authentication.

For information on how to obtain your subscription ID and generate and upload a
certificate file, see the following page [Generating and uploading a
certificate file and obtaining subscription ID](https://libcloud.readthedocs.org/en/latest/compute/drivers/azure.html#generating-and-uploading-a-certificate-file-and-obtaining-subscription-id).

* ``storage.name`` - Your storage account name.
* ``storage.access_key`` - Your storage account access key.

For information on how to obtain those credentials, see the following page
[Connecting to Azure Blobs](https://libcloud.readthedocs.org/en/latest/storage/drivers/azure_blobs.html#connecting-to-azure-blobs).

For usage of the Resource Manager actions you will need to create a [Service Principal](https://azure.microsoft.com/en-us/documentation/articles/resource-group-create-service-principal-portal/)

## Actions

### Virtual Machines / Servers

* ``list_vms`` - List available VMs.
* ``create_vm`` - Create a new VM.
* ``reboot_vm`` - Reboot a VM.
* ``destroy_vm`` - Destroy a VM.

### Object Storage

* ``list_containers`` - List containers.
* ``list_container_objects`` - List container objects.
* ``upload_file`` - Upload local file to the provided container.
* ``delete_object`` - Delete the provided object.

### Resource Management

* ``create_resource`` - Create a generic ARM resource
* ``create_linked_resource_url`` - Create a linked (template and parameter) resource from a URI
* ``list_resource_groups`` - List the names of the resource groups