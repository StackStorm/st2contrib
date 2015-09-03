# Octopus Deploy Integration Pack

This integration pack allows you to integrate with
[Octopus Deploy](http://octopusdeploy.com/).

## Actions

Currently, the following actions listed bellow are supported:

### Releases

* Create a new release - `create_release`
* Deploy a release to an environment - `deploy_release`
* Get a list of releases for a project - `get_releases`

## Configuration

Update config.yaml to setup the connection to Octopus.

* api_key - an API key generated in Octopus for your user http://docs.octopusdeploy.com/display/OD/How+to+create+an+API+key 
* host - the hostname of your Octopus server e.g. octopus.mydomain.com
* port - the port your API service is running on, 443 by default
