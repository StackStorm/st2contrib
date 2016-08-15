[![Apache ZooKeeper](./logo.png)](https://zookeeper.apache.org/)

# Apache ZooKeeper Integration Pack

Pack which allows integration with Apache ZooKeeper.

## Configuration

You will need to adjust the configuration in [config.yaml](./config.yaml).

* `zookeeper_hosts`: a comma-separated list of ZooKeeper hosts (including ports)
* `zookeeper_root`: the root node to use for all ZooKeeper operations in StackStorm

## Actions

Action                      | Description                           | Example or Use Case
--------------------------- | ------------------------------------- | ---------------------------------
**non_blocking_lease**      | Exclusive lease that does not block.  | Run cron on single St2 node in HA
