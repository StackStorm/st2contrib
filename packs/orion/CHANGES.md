# Changelog

# 0.5 (In dev)

- Renamed node_pollnow action to nodes_pollnow and extended it to
  support multiple nodes, count of polls and a pause between them.
- Added list_nodes_by_poller action.
- Added update_node_poller action.
- Added list_nodes_by_status action.
- Add drain_poller workflow.
- Fix naming of node_unmanage and node_remanage.

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
