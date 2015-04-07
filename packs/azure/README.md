# Microsoft Azure Integration Pack

Pack which contains integrations for different Microsoft Azure services.

## Configuration

* ``subscription_id`` - Your Azure subscription ID.
* ``cert_file`` - Path to the certificate file used for authentication.

For information on how to obtain your subscription ID and generate and upload a
certificate file, see the following page [Generating and uploading a
certificate file and obtaining subscription ID](https://libcloud.readthedocs.org/en/latest/compute/drivers/azure.html#generating-and-uploading-a-certificate-file-and-obtaining-subscription-id).

## Actions

### Virtual Machines / Servers

* ``list_vms`` - List available VMs.
* ``create_vm`` - Create a new VM.
* ``reboot_vm`` - Reboot a VM.
* ``destroy_vm`` - Destroy a VM.
