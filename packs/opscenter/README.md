# Datastax opscenter Integration Pack

This StackStorm Opscenter pack provides integrations to Datastax opscenter product via
opscenter APIs. At the time of writing this pack, http://docs.datastax.com/en/
opscenter/5.1/api/docs/index.html was used.

## Configuration

You'll need to setup base url for opscenter deployment and cluster_id that you want to work with in config.yaml.

```yaml
---
opscenter_base_url: http://myopscenter.mydomain.com:8888
cluster_id: "TestCluster"
```

## Actions

cluster_id in most of these actions are optional and is read from config.yaml. If you are
operating multiple clusters with same opscenter, be sure to explicitly provide the
`cluster_id` argument for the actions.

### General actions

`get_cluster_configs` - Lists configurations of all clusters managed by opscenter.

### Cluster actions

`get_cluster_info` - Lists info about specified cluster.

`start_cluster_repair` - Starts repair operation in specified cluster.

`get_repair_status` - Get status of repair operation in specified cluster.

`get_cluster_repair_progress` - Get repair progress for specified cluster.

`restart_cluster` - Restarts the specified cluster.

`get_nodes_info` - Dumps info about all nodes in cluster.

`get_storage_capacity` - Lists info about storage capacity of specified cluster.

### Node actions

For node actions, node_ip argument is mandatory.

`decommission_node` - Decommissions a node from cluster.

`drain_node` - Drains a Cassandra node.

`start_node` - Starts the specified node.

`stop_node` - Stops the specified node.

`restart_node` - Restarts the specified node.

`set_node_conf` - Sets configuration for specified node.

`get_node_conf` - Dumps configuration for specified node.


### Helper actions

`get_request_status` - Some actions return a request id. You can query
    status of request using this action.

`cancel_request` - Cancel a long running request.

`list_requests` - List all outstanding requests for a request type.

## Sensors

`EventsConsumer` - Consumes all events from opscenter and injects them into StackStorm
    with trigger ref as `opscenter.event` and payload as event info. Please see sensors/events_consumer.yaml for event specification.
