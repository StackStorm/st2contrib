[![Apache ZooKeeper](./logo.png)](https://zookeeper.apache.org/)

# Apache ZooKeeper Integration Pack

Pack which allows integration with Apache ZooKeeper.

## Configuration

Copy the example configuration in [zookeper.yaml.example](./zookeeper.yaml.example)
to `/opt/stackstorm/configs/zookeeper.yaml` and edit as required.

It must contain:

* `zookeeper_hosts`: a comma-separated list of ZooKeeper hosts (including ports)
* `zookeeper_root`: the root node to use for all ZooKeeper operations in StackStorm

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.


## Actions

Action                      | Description                           | Example or Use Case
--------------------------- | ------------------------------------- | ---------------------------------
**non_blocking_lease**      | Exclusive lease that does not block.  | Run cron on single St2 node in HA
