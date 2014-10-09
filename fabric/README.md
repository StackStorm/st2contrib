Fabric Integration
=================

##Introduction
This integration pack will take existing fabfiles and convert the Fabric tasks in to ST2 actions.

##Setup
The conversion script requires your fabfile to be in the lib directory of the fabric content pack.

##Installation
Once the fabfile is in place, run the following command:
	python metagenerator.py

This will generate the json files for all tasks in the fabfile.  You can now either manually add the actions with:
	st2 action create </path/to/json>
Or you can reload all content and they will get picked up.

##Known Issues
TBD
