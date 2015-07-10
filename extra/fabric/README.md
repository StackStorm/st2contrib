Fabric Integration
=================

##Introduction
This integration pack will take existing fabfiles and convert the Fabric tasks in to ST2 actions.

##Setup

To use this conversion script, copy the entire fabric directory into your newly named pack.

```
  cp st2contrib/extra/fabric /opt/stackstorm/packs/new_pack_name
```

Then, copy your `fabfile` into the `actions/lib` directory of your new pack.

```
  cp fabfile.py /opt/stackstorm/packs/new_pack_name/actions/lib
```

##Installation

Once the fabfile is in place, run the following command:
	
```
python metagenerator.py
```

This will generate the json files for all tasks in the fabfile.  You can now either manually add the actions with:
	st2 action create </path/to/json>
Or you can reload all content and they will get picked up.

##Known Issues

* Formatter sometimes creates immutable attributes without default values, preventing loading of newly created action metadata
