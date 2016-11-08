# Victorops

This action enables the integration of Victorops into stackstorm. It is capable of performing the following actions
1. Launch an incident by giving `severity ('INFO', 'WARNING', 'CRITICAL')`, `entity` and a `message` 
2. Send acknowledgment of any incident using its `entity` id and a `message` indicating acknowledgment
3. Recover an incident by giving `entity` id and a `message` indicating how the incident was recovered

# Configuration

Copy the example configuration in [victorops.yaml.example](./victorops.yaml.example)
to `/opt/stackstorm/configs/victorops.yaml` and edit as required.

It must contain:

* `api_key`` - API token for Victorops integration - see below
* `routing_key` - An API token generated in the admin interface

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## How to get API key

Once you sign in to your Victorops account go to the settings tab and click in Integrations button. A table will come at the right side, click on REST endpoint, It will spit out a Post URL, you just need to copy the part after `generic` becuase the first part is same for all. Copy and paste that part of API key in the config.yaml file.
![Alt text](/st2contrib/_images/api_key.png?raw=true "add API key")


## How to get Routing Key

Routing key routes the incident information to the team  that you mention. If there is one team/group you can mention it in config file otherwise you can pass an optional parameter of `notify_group` when opening an incident to notify any other team/group for any incident. Mention one routing key in config file so that if you dont want to pass parameter again and again it will be picked up by default from config file. The process of adding routing key is described below:

Now to get the routing key you need to scroll down and you will see `Incident Routing` section. Click on `Add Rule`, then add the name of routing key and select the team to which you want to route the incident to. Once thats done copy the name that you just gave in routing key and paste it into the `config.yaml` file. The following images illustrate the steps.
![Alt text](/st2contrib/_images/add_rule.png?raw=true "add Rule")
![Alt text](/st2contrib/_images/routing_key.png?raw=true "add routing key")
![Alt text](/st2contrib/_images/done.png?raw=true "select team to route the incidents to")


## Actions

* `ack_incident` - Acknowledge a triggered event on victorops
* `open_incident` - Triggers the event on VictorOps with the given parameters
* `recover_incident` - Recover a triggered event on victorops
