# DigitalOcean Integration Pack

This pack allows for DigitalOcean integrations.

## Configuration

Copy the example configuration in [digitalocean.yaml.example](./digitalocean.yaml.example)
to `/opt/stackstorm/configs/digitalocean.yaml` and edit as required.

It must contain:

* ``token`` - An API token generated in the admin interface

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Actions

* ``get_action``
* ``get_all_domains``
* ``get_all_droplets``
* ``get_all_images``
* ``get_all_regions``
* ``get_all_sizes``
* ``get_all_sshkeys``
* ``get_data``
* ``get_domain``
* ``get_droplet``
* ``get_global_images``
* ``get_get_image``
* ``get_get_my_images``
* ``get_ssh_key``
