# Changelog

# 0.5

- Renamed node_pollnow action to nodes_pollnow and extended it to
  support multiple nodes, count of polls and a pause between them.
- Added list_nodes_by_poller action.
- Added update_node_poller action.
- Added list_nodes_by_status action.
- Add drain_poller workflow.
- Fix naming of node_unmanage and node_remanage.
- Migrate config.yaml to config.schema.yaml.
  - Due to this migration only a single Orion platform is now supported.
  - For SNMP Communities the speical values `internal` and `customer`
    will be replaced with the config values.
- Remove std_communtity parameter from node_create and use the
  standard function.

# 0.3.1

- In the Orion.node_status alais set the color for the result so it
  reflects it status.

# 0.3

- Added the following actions:
   - node_create (tbc).
   - node_remanage.
   - node_unmanage.
   - node_custom_prop_list (tbc).
   - ncm_node_add (tbc).
   - node_custom_prop_update (tbc).
- Renamed action status to node_status.
- Fixes to ncm_config_download action & alias.

## 0.1

- Added action & alias status.
- Added action & alias ncm_config_download.
