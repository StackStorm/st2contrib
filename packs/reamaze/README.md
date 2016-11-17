# reamaze Integration Pack

StackStorm integration with reamaze, a SaaS KB and Support Tool

## Configuration

Ideally, you should create a service/daemon account for this integration.

Copy the example configuration in [reamaze.yaml.example](./reamaze.yaml.example)
to `/opt/stackstorm/configs/reamaze.yaml` and edit as required.

* `brand` - Scoped brand to send API requests against
* `email` - Email of user connecting to reamaze
* `api_token` - Personal Token of user connecting

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Actions

* `reamaze.article_search` - Search through articles in KB and return results
