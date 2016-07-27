# VSphere Integration Pack

This pack integrates with vsphere and allows for the creation and management of Virtual Machines.

## Connection Configuration

You will need to specificy the details of the vcenter instance you will be connecting to within the `config.yaml` file.
You can specificy multiple environments using nested values

```yaml
  vsphere:
    dev:
      host:
      port:
      user:
      passwd:
    staging:
      host:
      port:
      user:
      passwd:
```
Note: To ensure backward compatability and ease for single environment use. If no vsphere value is passed to the actions it will look for v0.3 config.yaml structure:
```yaml
  host:
  port:
  user:
  passwd:
```

Please Note Configuration validation will raise an exception if config.yaml contains 'vsphere' but no defined endpoints.

## Todo
* Create actions for vsphere environment data retrieval. Allowing for integration with external systems for accurate action calls with informed parameter values.
* Review and implement ST2 1.5 config.yaml changes. Review how useable dynamic configuration can be in case of this Packs purpose.
* Expand base test files. Level of mocking required has limited this at present.

## Requirements
This pack requires the python module PYVMOMI. At present the `requirements.txt` specifies version 5.5.0. 
The version specification is to ensure compatibility with Python 2.7.6 (standard version with Ubuntu 14.04).
PYVMOMI 6.0 requires alternative connection coding and Python 2.7.9 minimum due to elements of the SSL module being used.

## Actions

* `vsphere.vm_end_items_get` - Retrieve json list of objects from vsphere
* `vsphere.vm_hw_basic_build` - Minstral Flow to Build Basic Server and power it on.
* `vsphere.vm_hw_cpu_mem_edit` - Adjust the CPU and RAM values assigned to a Virtual Machine
* `vsphere.vm_hw_detail_get` - Retrieve Vsphere Data about a virtual machine
* `vsphere.vm_hw_hdd_add` - Add a HardDrive Object to a Virtual Machine
* `vsphere.vm_hw_nic_add` - Add a Network Device to VM and attach to designated network.
* `vsphere.vm_hw_nic_edit` - Edit Network Device on Virtual machine (V0.2 only allows to switch network)
* `vsphere.vm_hw_power_off` - Perform VM Power off - Equivilant of Holding power button
* `vsphere.vm_hw_power_on` - Power on Virtual Machine
* `vsphere.vm_hw_scsi_controller_add` - Add SCSI HDD Controller device to VM
* `vsphere.vm_hw_uuid_get` - Retrieve VM UUID
* `vsphere.vm_hw_moid_get` - Retrieve VM MOID

## Known Bugs
* Bug: vm_hw_hdd_add, Specifying datastore does not work. New files will be added to the same datastore as the core VM files. Note. Specifying a Datastore Cluster does still install files to the correct set of datastores.
